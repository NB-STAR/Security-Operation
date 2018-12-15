## 一、账号设置
以专门的用户帐号和用户组运行 Apache 服务。

根据需要，为 Apache 服务创建用户及用户组。如果没有设置用户和组，则新建用户，并在 Apache 配置文件中进行指定。

创建 Apache 用户组。

`groupadd apache`

创建 Apache 用户并加入 Apache 用户组。

`useradd apache –g apache`

将下面两行设置参数加入 Apache 配置文件 httpd.conf 中：
```
User apache
Group apache
```
检查 `httpd.conf` 配置文件中是否允许使用非专用账户（如 root 用户）运行 Apache 服务。

默认设置一般即符合要求。Linux 系统中默认使用 apache 或者 nobody 用户，Unix 系统默认使用 daemon 用户。

## 二、授权设置
严格控制 Apache 主目录的访问权限，非超级用户不能修改该目录中的内容。

Apache 的 主目录对应于 Apache Server配置文件 httpd.conf 中的 Server Root 控制项，应设置为：

```
Server Root /usr/local/apache
```
判定条件： 非超级用户不能修改该目录中的内容。
检测操作： 尝试进行修改，看是否能修改该目录中的内容。

该目录一般设置为 `/etc/httpd` 目录，默认情况下属主为 root 用户，其它用户不能修改该目录中的文件。默认设置一般即符合要求。

严格设置配置文件和日志文件的权限，防止未授权访问。

执行`chmod 600 /etc/httpd/conf/httpd.conf`命令设置配置文件为属主可读写，其他用户无读写权限。
执行`chmod 644 /var/log/httpd/*.log`命令设置日志文件为属主可读写，其他用户拥有只读权限。

注意：

`/etc/httpd/conf/httpd.conf` 配置文件的默认权限是644，可根据需要修改权限为`600`。
`/var/log/httpd/*.log` 日志文件的默认权限为644，默认设置即符合要求。
三、日志设置
Apache 设备应配置日志功能，对运行错误、用户访问等事件进行记录，记录内容包括时间，用户使用的 IP 地址等内容。

修改 `httpd.conf` 配置文件，设置日志记录文件、记录内容、记录格式。

错误日志：
```
  LogLevel notice #日志的级别
  ErrorLog /…/logs/error_log #日志的保存位置(错误日志)
```
访问日志：
```
  LogFormat %h %l %u %t \”%r\” %>s %b “%{Accept}i\”%{Referer}i\” \”%{User-Agent}i\””
  combined
  CustomLog /…/logs/access_log combined (访问日志)
```
注意：

`ErrorLog`指令设置错误日志文件名和位置。错误日志是最重要的日志文件。Apache httpd 程序将在这个文件中存放诊断信息和处理请求中出现的错误。若要将错误日志传送到 Syslog，则执行ErrorLog syslog命令。

`CustomLog`指令指定了保存日志文件的具体位置以及日志的格式。访问日志中会记录服务器所处理的所有请求。
`LogFormat`命令用于设置日志格式，建议设置为 combined 格式。

`LogLevel`命令用于调整记录在错误日志中的信息的详细程度，建议设置为 `notice`。日志的级别，默认是 warn 级别，notice 级别比较详细，但在实际中由于日志会占用大量硬盘空间。

## 四、禁止访问外部文件
禁止 Apache 访问 Web 目录之外的任何文件。

修改 httpd.conf 配置文件。
```
 Order Deny,Allow
 Deny from all
```
设置可访问的目录。
```
 Order Allow,Deny
 Allow from /web
```
说明： 其中 /web 为网站根目录。

默认配置如下，可根据您的业务需要进行设置。
```
 Options FollowSymLinks
 Allow Override None
```
## 五、禁止目录列出
目录列出会导致明显信息泄露或下载，建议禁止 Apache 列表显示文件。在 `/etc/httpd/httpd.conf` 配置文件中删除 `Options` 的 `Indexes` 设置即可。

修改 httpd.conf 配置文件：
```
 #Options Indexes FollowSymLinks #删掉Indexes
 Options FollowSymLinks
 AllowOverride None
 Order allow,deny
 Allow from all
```
将`Options Indexes FollowSymLinks`中的Indexes去掉，就可以禁止 Apache 显示该目录结构。Indexes的作用就是当该目录下没有 index.html 文件时，自动显示目录结构。

重新启动 Apache 服务。

六、错误页面重定向
Apache 错误页面重定向功能可以防止敏感信息泄露。

修改 httpd.conf 配置文件：
```
 ErrorDocument 400 /custom400.html
 ErrorDocument 401 /custom401.html
 ErrorDocument 403 /custom403.html
 ErrorDocument 404 /custom404.html
 ErrorDocument 405 /custom405.html
 ErrorDocument 500 /custom500.html
```
注意： `Customxxx.html` 为要设置的错误页面。

重新启动 Apache 服务。

注意： 此项配置需要应用系统设有错误页面，或者不在 httpd 中设置，而完全由业务逻辑实现。

## 七、拒绝服务防范

根据业务需要，合理设置 `session` 时间，防止拒绝服务攻击。

修改 httpd.conf 配置文件:
```
 Timeout 10 #客户端与服务器端建立连接前的时间间隔
 KeepAlive On
 KeepAliveTimeout 15 #限制每个 session 的保持时间是 15 秒 注：此处为一建议值，具体的设定需要根据现实情况。
```
重新启动 Apache 服务。

注意： 默认值为Timeout 120，KeepAlive Off，KeepAliveTimeout 15，该项设置涉及性能调整。

## 八、隐藏 Apache 的版本号
隐藏 Apache 的版本号及其它敏感信息。

修改 httpd.conf 配置文件：
```
ServerSignature Off ServerTokens Prod
```
## 九、关闭 TRACE功能

关闭 TRACE 功能，防止 TRACE 方法被访问者恶意利用。

在 /etc/httpd/conf/httpd.conf 配置文件中添加以下设置参数：

TraceEnable Off
注意： 该参数适用于 Apache 2.0 以上版本。

十、禁用 CGI
如果服务器上不需要运行 CGI 程序，建议禁用 CGI。

如果没有CGI程序，可以修改 /etc/httpd/conf/httpd.conf 配置文件，把 cgi-bin 目录的配置和模块都进行注释。
```
#LoadModule cgi_module modules/mod_cgi.so
#ScriptAlias /cgi-bin/ “/var/www/cgi-bin/”
#
#AllowOverride None
# Options None
#Order allow,deny
#Allow from all
#
```
## 十一、绑定监听地址
服务器有多个 IP 地址时，只监听提供服务的 IP 地址。

执行以下命令查看是否绑定 IP 地址。
```
 cat /etc/httpd/conf/httpd.conf|grep Listen
```
修改 /etc/httpd/conf/httpd.conf 配置文件。
```
 Listen x.x.x.x:80
```
监听功能默认监听所有地址，如果服务器只有一个 IP 地址可不修改该项设置，如果有多个 IP 可根据需要进行设置。

## 十二、删除缺省安装的无用文件
删除缺省安装的无用文件。

删除缺省 HTML 文件：
```
  # rm -rf /usr/local/apache2/htdocs/*
```
删除缺省的 CGI 脚本：
```
  # rm –rf /usr/local/apache2/cgi-bin/*
```
删除 Apache 说明文件：
```
  # rm –rf /usr/local/apache2/manual
```
删除源代码文件：
```
  # rm -rf /path/to/httpd-2.2.4*
```
删除 CGI。

可根据实际情况删除，一般情况下 /var/www/html /var/www/cgi-bin 默认就是空的。

注意： 根据安装步骤不同和版本不同，某些目录或文件可能不存在或位置不同。

## 十三、禁用非法 HTTP 方法
禁用 PUT、DELETE 等危险的 HTTP 方法。

修改 httpd.conf 配置文件，只允许 get、post 方法。
```
<Location />  
<LimitExcept GET POST CONNECT OPTIONS> 
  Order Allow,Deny 
  Deny from all 
</LimitExcept> 
</Location>
```
可根据需要进行设置，如果需要用到 PUT 或 Delete 等 HTTP 方法的话，在 /etc/httpd/conf/httpd.conf 配置文件中相应添加即可。