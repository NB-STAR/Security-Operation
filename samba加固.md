Samba是在Linux和UNIX系统上实现SMB协议的一个软件。2017年5月24日Samba发布的4.6.4版本修复了一个严重的远程代码执行漏洞。漏洞编号为CVE-2017-7494，影响Samba 3.5.0 之后及4.6.4/4.5.10/4.4.14版本。

1. 使用源码安装的Samba用户，请尽快下载最新的Samba版本手动更新；

2. 使用二进制分发包（RPM等方式）的用户立即进行yum，apt-get update等安全更新操作；

缓解策略：用户可以通过在smb.conf的[global]节点下增加 “nt pipe support = no” 选项，然后重新启动Samba服务， 以此达到缓解该漏洞的效果。