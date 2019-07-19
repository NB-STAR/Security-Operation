## 0. 了解ssh

SSH 主要由三部分组成：

传输层协议 [SSH-TRANS]
提供了服务器认证，保密性及完整性。此外它有时还提供压缩功能。 SSH-TRANS 通常运行在TCP/IP连接上，也可能用于其它可靠数据流上。 SSH-TRANS 提供了强力的加密技术、密码主机认证及完整性保护。该协议中的认证基于主机，并且该协议不执行用户认证。更高层的用户认证协议可以设计为在此协议之上。

用户认证协议 [SSH-USERAUTH]
用于向服务器提供客户端用户鉴别功能。它运行在传输层协议 SSH-TRANS 上面。当SSH-USERAUTH 开始后，它从低层协议那里接收会话标识符（从第一次密钥交换中的交换哈希H ）。会话标识符唯一标识此会话并且适用于标记以证明私钥的所有权。 SSH-USERAUTH 也需要知道低层协议是否提供保密性保护。

连接协议 [SSH-CONNECT]
将多个加密隧道分成逻辑通道。它运行在用户认证协议上。它提供了交互式登录话路、远程命令执行、转发 TCP/IP 连接和转发 X11 连接。

SSH是由客户端和服务端的软件组成的，有两个不兼容的版本分别是：1.x和2.x。 用SSH 2.x的客户程序是不能连接到SSH 1.x的服务程序上去的。OpenSSH 2.x同时支持SSH 1.x和2.x。

服务端是一个守护进程(daemon)，他在后台运行并响应来自客户端的连接请求。服务端一般是sshd进程，提供了对远程连接的处理，一般包括公共密钥认证、密钥交换、对称密钥加密和非安全连接。

客户端包含ssh程序以及像scp（远程拷贝）、slogin（远程登陆）、sftp（安全文件传输）等其他的应用程序。

他们的工作机制大致是本地的客户端发送一个连接请求到远程的服务端，服务端检查申请的包和IP地址再发送密钥给SSH的客户端，本地再将密钥发回给服务端，自此连接建立。SSH 1.x和SSH 2.x在连接协议上有一些差异。

一旦建立一个安全传输层连接，客户机就发送一个服务请求。当用户认证完成之后，会发送第二个服务请求。这样就允许新定义的协议可以与上述协议共存。连接协议提供了用途广泛的各种通道，有标准的方法用于建立安全交互式会话外壳和转发（“隧道技术”）专有 TCP/IP 端口和 X11 连接。

SSH被设计成为工作于自己的基础之上而不利用超级服务器(inetd)，虽然可以通过inetd上的tcpd来运行SSH进程，但是这完全没有必要。启动SSH服务器后，sshd运行起来并在默认的22端口进行监听（你可以用 # ps -waux | grep sshd 来查看sshd是否已经被正确的运行了）如果不是通过inetd启动的SSH，那么SSH就将一直等待连接请求。当请求到来的时候SSH守护进程会产生一个子进程，该子进程进行这次的连接处理 。

## 1. 查看ssh服务的状态

输入以下命令：

`sudo service sshd status`

如果出现

`Loaded: error (Reason: No such file or directory)`

提示的话，说名没有安装ssh服务，按照第二步：安装ssh服务。

如果出现

`Active: inactive (dead)`

说明已经安装了ssh服务，但是没有开启。按照第三步：开启ssh服务。

## 2. 安装ssh服务

安装ssh命令：

如果你用的是redhat，fedora，centos等系列linux发行版，那么敲入以下命令：

`sudo yum install openssh-server -y`

如果你使用的是debian，ubuntu，linux mint等系列的linux发行版，那么敲入以下命令：

`sudo apt-get install openssh-server -y`

然后按照提示，安装就好了。

## 3.开启ssh服务

在终端敲入以下命令：

`sudo service sshd start`

执行完命令后，用第一步：查看ssh服务状态的命令，如果出现以下提示

`Active: active (running) since xxxxx; xxs ago`

或者使用

`ps -e | grep ssh`

看到有ssh字样，说明已启动，如果没有就手动启动

/etc/init.d/ssh start

说明你的ssh服务已经启动了。如果失败来的话，那试着卸载一下（看第五步：卸载ssh服务）再安装（第二步：安装ssh服务）。

## 4. 使用ssh服务

Windows 推荐安装 xshell 使用

linux或者mac下，直接使用 `ssh user@ip`


## 5. 卸载ssh服务

如果你用的是redhat，fedora，centos等系列linux发行版，那么敲入以下命令：

`sudo yum remove openssh-server`

如果你使用的是debian，ubuntu，linux mint等系列的linux发行版，那么敲入以下命令：

`sudo apt remove openssh-server`

然后就会提示卸载完成。

## 6. 安全配置ssh-server

配置文件位于/etc/ssh/sshd_config


**访问地址控制**

将root账户仅限制为控制台访问，不允许ssh登录

`vim /etc/ssh/sshd_config`

```
PermitRootLogin no
systemctl restart ssh.service
```

配置TCP Wrappers ，对远程主机进行访问控制，修改/etc/hosts.deny拒绝所有远程主机访问sshd服务，然后修改/etc/hosts.allow仅允许特定主机/网络段使用sshd服务

修改hosts.deny文件`vim /etc/hosts.deny`

`sshd: ALL   # ALL为所有地址 `

修改hosts.allow文件`vim /etc/hosts.allow`

`sshd: 192.168.1. # 仅允许192.168.1.x网段访问`  

 
**通过控制用户帐号，限制其对ssh的访问**

`vim /etc/ssh/sshd_config`

在该文件的最后添加以下两行

```
// 允许的用户
AllowUsers  xctf 

// 禁止hacker登录，和禁止xctf使用192.168.5.10的ip地址登录
DenyUsers   hacker xctf@192.168.5.10   
```

`systemctl restart ssh.service    //重启ssh服务`


**强制使用SSH Protocol2（版本1不安全）**

`vim /etc/ssh/sshd_config`

```
Protocol 2

systemctl restart ssh.service
```

 
**不支持闲置会话，并配置idle Logout Timeout 间隔**

`vim /etc/ssh/sshd_config`

编辑以下两行

```
ClientAliveInterval 600      // 600为秒，即600秒后无动作就自动断开连接

ClientAliveCountMax 3
```

`systemctl restart ssh.service   // 重启ssh服务`

 

**禁止使用空密码登录，设置最大尝试登录次数**

`vim /etc/ssh/sshd_config`

编辑以下三行

```
PermitEmptyPasswords no

PasswordAuthentication yes

MaxAuthTries 6     // 尝试次数6次
```

`systemctl restart ssh.service`

 

**禁用基于主机的身份验证**

`vim /etc/ssh/sshd_config`

```
HostbasedAuthentication no
```

`systemctl restart ssh.service`

 
**禁用用户的 .rhosts 文件**

`vim /etc/ssh/sshd_config`

```
IgnoreRhosts yes
```

`systemctl restart ssh.service`


**限制ssh，将侦听绑定到指定的可用网络接口与端口**

`vim /etc/ssh/sshd_config`

```
ListenAddress 192.168.0.3

Port 56175      //可以修改ssh的端口
```
 
**始终保持ssh补丁版本最新（可以设置到任务计划中）**

`yum/apt update openssh-server openssh openssh-clients -y`