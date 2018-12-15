# MySQL服务安全加固


## 漏洞发现

### 判断Mysql数据库版本

nmap的指纹识别可以精确的判断数据库的版本号，而metasploit提供的模块的特点就是能够判断数据库是否允许外链
```
msf > use auxiliary/scanner/mysql/mysql_version
msf auxiliary(mysql_version) > set RHOSTS [ip]
```
### 如果允许外链则可以显示版本号

如果数据库允许外链，则能暴力破解密码
这个模块没有默认字典，上网下个字典，或者使用kali自带的字典
```
msf > use auxiliary/scanner/mysql/mysql_login

set USERNAME root

set PASS_FILE [字典的路径]
```

### 枚举数据库信息
```
msf > use auxiliary/admin/mysql/mysql_enum
show options
```
枚举的信息包括mysql版本号，操作系统架构，路径和密码hash等一些信息

### Mysql认证漏洞利用
这个模块利用的是CVE-2012-2122，在一次测试网易的过程中发现一枚，提交给NSRC了。

mysql任意用户密码概率登陆漏洞，按照公告说法大约256次就能够蒙对一次、All MariaDB and MySQL versions up to 5.1.61, 5.2.11, 5.3.5, 5.5.22 are vulnerable.

CVE ID: CVE-2012-2122

MariaDB是为MySQL提供偶然替代功能的数据库服务器。MySQL是开源数据库。

MariaDB 5.1.62, 5.2.12、5.3.6、5.5.23之前版本和MySQL 5.1.63、5.5.24、5.6.6之前版本在用户验证的处理上存在安全漏洞，可能导致攻击者无需知道正确口令就能登录到MySQL服务器。

用户连接到MariaDB/MySQL后，应用会计算和比较令牌值，由于错误的转换，即使memcmp()返回非零值，也可能出现错误的比较，造成MySQL/MariaDB误认为密码是正确的，因为协议使用的是随机字符串，该Bug发生的几率为1/256。MySQL的版本是否受影响取决于程序的编译方式，很多版本（包括官方提供的二进制文件）并不受此漏洞的影响。

也就是说只要知道用户名，不断尝试就能够直接登入SQL数据库。按照公告说法大约256次就能够蒙对一次。

```
msf > use auxiliary/admin/mysql/mysql_autobypass_hashdump

show options

set RHOSTS [ip]

exploit
```

### UDF提权
Metasploit提供的exploit适应于5.5.9以下


0x07.利用Mof提权
这个模块的好处是通过用户名和密码可以直接返回一个meterpreter会话
```
msf > use exploit/windows/mysql/mysql_mof

set rhost [ip]

set USERNAME root

set PASSWORD xxx

exploit
```

## 安全加固

### 帐号安全

禁止 Mysql 以管理员帐号权限运行

以普通帐户安全运行 mysqld，禁止以管理员帐号权限运行 MySQL 服务。在 /etc/my.cnf 配置文件中进行以下设置。
```
[mysql.server]
user=mysql
```
### 避免不同用户间共享帐号

参考以下步骤。

创建用户。
```
mysql> mysql> insert into
mysql.user(Host,User,Password,ssl_cipher,x509_issuer,x509_sub 
ject) values("localhost","pppadmin",password("passwd"),'','','');
```
执行以上命令可以创建一个 phplamp 用户。

使用该用户登录 MySQL 服务。
```
mysql>exit; 
@>mysql -u phplamp -p 
@>输入密码 
mysql>登录成功
删除无关帐号
```

DROP USER 语句可用于删除一个或多个 MySQL 账户。使用 DROP USER 命令时，必须确保当前账号拥有 MySQL 数据库的全局 CREATE USER 权限或 DELETE 权限。账户名称的用户和主机部分分别与用户表记录的 User 和 Host 列值相对应。

执行DROP USER user;语句，您可以取消一个账户和其权限，并删除来自所有授权表的帐户权限记录。

### 口令

检查账户默认密码和弱密码。口令长度需要至少八位，并包括数字、小写字母、大写字母和特殊符号四类中的至少两种类型，且五次以内不得设置相同的口令。密码应至少每 90 天进行一次更换。

您可以通过执行以下命令修改密码。
```
 mysql> update user set password=password('test!p3') where user='root';
 mysql> flush privileges;
```
### 授权

在数据库权限配置能力范围内，根据用户的业务需要，配置其所需的最小权限。

查看数据库授权情况。
```
mysql> use mysql;
mysql> select * from user;
mysql>select * from db;
mysql>select * from host;
mysql>select * from tables_priv;
mysql>select * from columns_priv;
```
通过 revoke 命令回收不必要的或危险的授权。

```
mysql> help revoke
Name: 'REVOKE'
Description:
Syntax:
REVOKE
priv_type [(column_list)]
   [, priv_type [(column_list)]] ...
 ON [object_type]
     {
         *
       | *.*
       | db_name.*
       | db_name.tbl_name
       | tbl_name
       | db_name.routine_name
     }
 FROM user [, user] ...
```

### 开启日志审计功能

数据库应配置日志功能，便于记录运行状况和操作行为。

MySQL服务有以下几种日志类型：

错误日志： -log-err
查询日志： -log （可选）
慢查询日志： -log-slow-queries （可选）
更新日志： -log-update
二进制日志： -log-bin

找到 MySQL 的安装目录，在 my.ini 配置文件中增加上述所需的日志类型参数，保存配置文件后，重启 MySQL 服务即可启用日志功能。例如，
```
#Enter a name for the binary log. Otherwise a default name will be used. 
#log-bin= 
#Enter a name for the query log file. Otherwise a default name will be used. 
#log= 
#Enter a name for the error log file. Otherwise a default name will be used. 
log-error= 
#Enter a name for the update log file. Otherwise a default name will be used. 
#log-update=

```
该参数中启用错误日志。如果您需要启用其他的日志，只需把对应参数前面的 “#” 删除即可。

日志查询操作说明

执行show variables like 'log_%';命令可查看所有的 log。
执行show variables like 'log_bin';命令可查看具体的 log。
安装最新补丁

确保系统安装了最新的安全补丁。

注意： 在保证业务及网络安全的前提下，并经过兼容性测试后，安装更新补丁。

如果不需要，应禁止远程访问

### 禁止网络连接，防止猜解密码攻击、溢出攻击、和嗅探攻击。

注意： 仅限于应用和数据库在同一台主机的情况。

如果数据库不需要远程访问，可以禁止远程 TCP/IP 连接，通过在 MySQL 服务器的启动参数中添加--skip-networking参数使 MySQL 服务不监听任何 TCP/IP 连接，增加安全性。

您可以使用 安全组 进行内外网访问控制，建议不要将数据库高危服务对互联网开放。

### 设置可信 IP 访问控制

通过数据库所在操作系统的防火墙限制，实现只有信任的 IP 才能通过监听器访问数据库。
```
 mysql> GRANT ALL PRIVILEGES ON db.*
 ·-> -> TO 用户名@'IP子网/掩码';
 ```
