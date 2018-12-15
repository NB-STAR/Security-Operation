## 1. 在Nginx中禁用server_tokens指令

该server_tokens指令告诉nginx的错误页面显示其当前版本。 这是不可取的，因为您不想与世界共享这些信息，以防止在您的Web服务器由特定版本中的已知漏洞造成的攻击。

要禁用server_tokens指令，设定在关闭服务器块内：
```
server {
listen       192.168.0.25:80;
Server_tokens        off;
server_name  howtoinglovesnginx.com www.howtoinglovesnginx.com;
access_log  /var/www/logs/howtoinglovesnginx.access.log;
error_log  /var/www/logs/howtoinglovesnginx.error.log error;
root   /var/www/howtoinglovesnginx.com/public_html;
index  index.html index.htm;
}
```

## 2. 在Nginx中禁用不需要的HTTP方法

对于一般的网站和应用程序，你应该只允许GET，POST，和HEAD并禁用所有其他人。

为此，将以下行代码放在服务器块中。 444 HTTP响应指空响应，并经常在Nginx的用来愚弄恶意软件攻击：
```
if ($request_method !~ ^(GET|HEAD|POST)$) {
return 444;
}
```

## 3. 在Nginx中设置缓冲区大小限制
为了防止对您的Nginx Web服务器的缓冲区溢出攻击，坐落在一个单独的文件以下指令（创建的文件名为/etc/nginx/conf.d/buffer.conf为例）：

```
client_body_buffer_size  1k;
client_header_buffer_size 1k;
client_max_body_size 1k;
large_client_header_buffers 2 1k;
```

上面的指令将确保对您的Web服务器的请求不会导致系统中的缓冲区溢出。

然后在配置文件中添加一个include指令：
```
include /etc/nginx/conf.d/*.conf;
```

## 4. 日志设置
查看nginx.conf配置文件中，error_log、access_log前的“#”是否去掉

将error_log前的“#”去掉，记录错误日志
将access_log前的“#”去掉，记录访问日志
设置access_log，修改配置文件如下：
```
log_format  nsfocus  '$remote_addr - $remote_user [$time_local] '
              ' "$request" $status $body_bytes_sent "$http_referer" '
              ' "$http_user_agent" "$http_x_forwarded_for"'; access_log  logs/access.log  nsfocus;  
``` 
nsfocus是设置配置文件格式的名称

## 5. 自定义错误信息

修改src/http/ngx_http_special_response.c，自己定制错误信息
```
## messages with just a carriage return.
static char ngx_http_error_400_page[] = CRLF;
static char ngx_http_error_404_page[] = CRLF;
static char ngx_http_error_413_page[] = CRLF;
static char ngx_http_error_502_page[] = CRLF;
static char ngx_http_error_504_page[] = CRLF;
```
常见错误：
```
400 bad request
404 NOT FOUND
413 Request Entity Too Large
502 Bad Gateway
504 Gateway Time-out
```

## 6. 手动安装补丁或安装最新版本软件