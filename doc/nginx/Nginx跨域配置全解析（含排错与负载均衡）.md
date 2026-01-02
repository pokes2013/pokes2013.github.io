# Nginx跨域配置全解析（含排错与负载均衡）

## 一、Nginx跨域核心原理

**Nginx跨域**，本质是利用**Nginx反向代理**能力，解决浏览器的**同源策略**限制，让前端页面能正常请求不同域名/端口下的后端接口。

### 1.核心概念详解

- **同源策略**：浏览器的安全机制，要求前端页面（`协议+域名+端口`三者完全一致）才能向目标服务器发起请求。例：`http://localhost:8080`的页面，直接请求`http://api.example.com:3000`会被浏览器拦截，提示**CORS错误**。

- **跨域问题的表现**：浏览器控制台会出现类似报错：
  
    ```bash
    `AccesstoXMLHttpRequestat'http://api.example.com'fromorigin'http://localhost:8080'hasbeenblockedbyCORSpolicy:No'Access-Control-Allow-Origin'headerispresentontherequestedresource.`
    ```
    
    
    
- **Nginx解决跨域的原理**：Nginx作为中间代理层，将前端的跨域请求**转发**到后端接口，再将后端响应**返回**给前端。对浏览器而言，请求的是**同域名的Nginx地址**，不存在跨域；对后端而言，请求来自Nginx代理，无需直接处理前端的跨域头。

### 2.Nginx解决跨域的两种常用配置

#### 方式1：直接添加CORS响应头

适合前端直接请求后端接口，通过Nginx注入跨域允许的响应头，无需转发。

```bash

server{
listen80;
server_nameexample.com;

#允许跨域的配置
location/api/{
#允许的源（*表示所有，生产环境建议指定具体域名）
add_headerAccess-Control-Allow-Origin*;
#允许的请求方法
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,OPTIONS';
#允许的请求头
add_headerAccess-Control-Allow-Headers'Content-Type,Authorization';

#预检请求（OPTIONS）直接返回204
if($request_method=OPTIONS){
return204;
}

#反向代理到后端接口
proxy_passhttp://127.0.0.1:3000;
proxy_set_headerHost$host;
proxy_set_headerX-Real-IP$remote_addr;
}
}
```

#### 方式2：反向代理转发（更常用）

前端请求Nginx的同域名地址，Nginx转发到后端，彻底规避浏览器跨域检测。

**场景**：前端`http://localhost:8080`→请求`http://localhost:80/api`→Nginx转发到`http://api.example.com:3000`

```bash

server{
listen80;
server_namelocalhost;

#前端页面的静态资源（如果前端部署在Nginx）
location/{
root/usr/share/nginx/html;#前端打包后的dist目录
indexindex.html;
try_files$uri$uri//index.html;#解决Vue/React路由刷新404
}

#代理后端接口，解决跨域
location/api/{
#转发到后端真实地址
proxy_passhttp://api.example.com:3000/;
#传递请求头（重要，后端需要获取真实的Host/IP）
proxy_set_headerHost$proxy_host;
proxy_set_headerX-Real-IP$remote_addr;
proxy_set_headerX-Forwarded-For$proxy_add_x_forwarded_for;
}
}
```

此时前端请求地址写`http://localhost/api/user`即可，浏览器认为是同源请求。

### 3.关键注意事项

1. 3.1、`Access-Control-Allow-Origin`不要滥用：生产环境需指定具体域名（如`http://www.example.com`），避免安全风险；若需支持多个域名，可通过Nginx变量动态判断。

2. 3.2、`OPTIONS`处理预检请求：前端发送`PUT/DELETE`等复杂请求时，会先发送`OPTIONS`预检请求，Nginx需直接返回`204`，否则会跨域失败。

3. 3.3、`/`反向代理的结尾问题：

    proxy_pass`结尾带`/`和不带`/`区别很大：

> `proxy_passhttp://api.example.com:3000/`→转发`http://localhost/api/user`→`http://api.example.com:3000/user`
>
> `proxy_passhttp://api.example.com:3000`→转发`http://localhost/api/user`→`http://api.example.com:3000/api/user`

## 二、Nginx跨域配置排错清单

这份清单按**"现象-原因-解决方案"**结构整理，覆盖90%以上的跨域配置问题，方便快速定位和修复。

|报错现象/问题表现|常见原因|解决方案|
|---|---|---|
|浏览器提示`No'Access-Control-Allow-Origin'headerispresent`|1.Nginx未配置`add_header`跨域头2.跨域头被后端接口覆盖3.配置的`location`不匹配请求路径|1.确认`location`路径与前端请求一致2.跨域头配置添加`always`参数：`add_headerAccess-Control-Allow-Origin*always;`3.检查后端是否返回了`Access-Control-Allow-Origin`，避免冲突|
|`OPTIONS`预检请求返回404/403|1.未处理`OPTIONS`请求2.服务器防火墙拦截`OPTIONS`方法|1.配置`if($request_method=OPTIONS){return204;}`2.确保`add_headerAccess-Control-Allow-Methods`包含`OPTIONS`3.检查防火墙/安全组是否放行`OPTIONS`请求|
|配置跨域头后仍报错`The'Access-Control-Allow-Origin'headercontainsmultiplevalues`|1.Nginx和后端同时返回了`Access-Control-Allow-Origin`头2.Nginx多个`location`重复配置跨域头|1.统一由Nginx或后端处理跨域头，不要两边都配2.检查Nginx配置文件，删除重复的`add_header`配置|
|反向代理后接口404|1.`proxy_pass`结尾的`/`配置错误2.`location`路径与后端接口路径不匹配|1.牢记规则：-`proxy_passhttp://127.0.0.1:3000`→转发路径包含`location`前缀-`proxy_passhttp://127.0.0.1:3000/`→转发路径去掉`location`前缀2.用`curlhttp://nginx地址/api/test`测试转发是否正常|
|携带Cookie时跨域失败（提示`Credentialsflagis'true'`）|1.`Access-Control-Allow-Origin`配置为`*`（不支持带Cookie）2.未配置`Access-Control-Allow-Credentials:true`|1.将`Access-Control-Allow-Origin`改为具体域名，如`http://www.example.com`2.添加配置：`add_headerAccess-Control-Allow-Credentialstrue;`3.前端请求需设置`withCredentials:true`|
|自定义请求头（如Token）被拦截|未配置`Access-Control-Allow-Headers`包含自定义头|1.配置`add_headerAccess-Control-Allow-Headers'Content-Type,Authorization,Token';`2.确保`OPTIONS`请求返回的头包含自定义字段|
|Nginx重启后配置不生效|1.配置文件有语法错误2.未重载Nginx配置（直接重启可能中断服务）|1.执行`nginx-t`检查配置语法2.用`nginx-sreload`平滑重载配置3.查看Nginx错误日志：`tail-f/var/log/nginx/error.log`|
|生产环境配置`*`后安全扫描告警|滥用通配符`*`，存在跨域安全风险|1.动态匹配允许的域名，示例配置：`map$http_origin$allow_origin{|
| ~^http://www.example.com$$http_origin; |||
| ~^http://admin.example.com$$http_origin; |||
| default""; |||
|}|||
|add_headerAccess-Control-Allow-Origin$allow_originalways;`2.禁止配置`*`+`Allow-Credentials:true`的组合|||
## 三、通用排错步骤

1. 先验证请求是否到达Nginx：执行`tail-f/var/log/nginx/access.log`，查看前端请求的`request_uri`和`status_code`，确认请求路径是否匹配配置的`location`。

2. **用curl模拟请求测试**：
    `#测试OPTIONS预检请求
    curl-XOPTIONS-H"Origin:http://localhost:8080"-Ihttp://nginx地址/api/test `

    查看响应头是否包含跨域字段

3. 检查Nginx版本兼容性：低版本Nginx（<1.7.5）的`add_header`指令在`return204`时不会生效，需升级Nginx或改用其他方式处理`OPTIONS`请求。


## 四、Nginx配置文件中添加跨域头

核心是通过`add_header`指令配置浏览器跨域所需的CORS相关头部，以下分场景给出可直接复用的配置，并解释关键细节。

### 1、基础场景：允许所有域名跨域（测试环境）

适合本地开发/测试，配置最简单，但**生产环境禁止使用**（存在安全风险）。

### 完整配置示例

```nginx

server{
listen80;
server_nameyour-domain.com;#替换为你的域名/IP

#匹配需要跨域的接口路径（如/api开头）
location/api/{
#1.允许的源（*表示所有域名）
add_headerAccess-Control-Allow-Origin*always;
#2.允许的请求方法（覆盖常见的GET/POST/PUT/DELETE等）
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,OPTIONS'always;
#3.允许的请求头（包含自定义头如Token/Authorization）
add_headerAccess-Control-Allow-Headers'Content-Type,Authorization,Token,X-Requested-With'always;

#4.处理OPTIONS预检请求（关键，否则复杂请求会失败）
if($request_method=OPTIONS){
return204;#直接返回204，无需转发到后端
}

#5.反向代理到后端真实接口（根据你的实际地址修改）
proxy_passhttp://127.0.0.1:3000;#后端服务地址
proxy_set_headerHost$host;
proxy_set_headerX-Real-IP$remote_addr;
}
}
```

### 2、生产环境：指定允许的域名（推荐）

禁止用`*`，需明确允许的前端域名，支持单个/多个域名：

#### 2.1、单个允许的域名

```nginx

server{
listen80;
server_nameyour-domain.com;

location/api/{
#仅允许http://frontend.your-domain.com跨域
add_headerAccess-Control-Allow-Originhttp://frontend.your-domain.comalways;
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,OPTIONS'always;
add_headerAccess-Control-Allow-Headers'Content-Type,Authorization'always;
add_headerAccess-Control-Allow-Credentialstruealways;#允许携带Cookie

if($request_method=OPTIONS){
return204;
}

proxy_passhttp://127.0.0.1:3000;
proxy_set_headerHost$host;
}
}
```

#### 2.2、多个允许的域名（动态匹配）

通过`map`指令配置白名单，只允许指定的多个域名跨域：

```nginx

#放在server块外部（http块内），定义域名白名单
map$http_origin$allow_origin{
~^http://frontend1.your-domain.com$$http_origin;#允许的域名1
~^http://frontend2.your-domain.com$$http_origin;#允许的域名2
default"";#其他域名拒绝
}

server{
listen80;
server_nameyour-domain.com;

location/api/{
#使用上面定义的动态变量
add_headerAccess-Control-Allow-Origin$allow_originalways;
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,OPTIONS'always;
add_headerAccess-Control-Allow-Headers'Content-Type,Authorization'always;
add_headerAccess-Control-Allow-Credentialstruealways;

if($request_method=OPTIONS){
return204;
}

proxy_passhttp://127.0.0.1:3000;
}
}
```

### 3、关键配置说明

3.1、`always`参数必须加：默认情况下，add_header只在响应码为200/201/204/301/302/304/307时生效，加always能确保所有响应（包括404/500等错误）都携带跨域头，避免前端报错。

3.2、`Access-Control-Allow-Credentials`：当需要前端请求携带Cookie/Token时，必须设为true，且Access-Control-Allow-Origin不能用`*`，必须指定具体域名。

3.3、OPTIONS预检请求：前端发送PUT/DELETE/带自定义头的请求时，浏览器会先发OPTIONS请求“预检”，Nginx需直接返回204，无需转发到后端，否则跨域会失败。

### 4、配置生效步骤

4.1、编辑Nginx配置文件（通常路径：`/etc/nginx/nginx.conf`或`/etc/nginx/conf.d/your-config.conf`）；

4.2、检查配置语法是否正确：`nginx-t`

4.3、平滑重载配置（不中断服务）：`nginx-sreload`

### 总结

1. 添加跨域头核心是用`add_header`配置`Access-Control-*`系列指令，`always`参数是必加项；

2. 测试环境可用`*`简化配置，生产环境必须指定具体域名，避免安全风险；

3. 务必处理OPTIONS预检请求，否则复杂跨域请求会失败。

## 五、多个域名跨域（生产级配置）

核心是通过Nginx的`map`指令定义域名白名单，动态匹配前端请求的Origin并返回对应的跨域头，既满足多域名需求，又保证生产环境的安全性。以下是可直接落地的生产级完整配置方案。

### 1、核心配置思路

1.1、使用`map`指令（放在`http`块内）定义「允许跨域的域名白名单」，匹配前端请求的`Origin`头；

1.2、在`server/location`块内引用`map`生成的变量，动态返回`Access-Control-Allow-Origin`；

1.3、强制开启`Access-Control-Allow-Credentials`（适配前端带Cookie/Token的场景）；

1.4、严格处理OPTIONS预检请求，避免跨域失败。

### 2、完整配置示例（可直接复制修改）

```nginx

#=====================第一步：定义域名白名单（放在http块内）=====================
#路径：/etc/nginx/nginx.conf或/etc/nginx/conf.d/default.conf
http{
#1.定义map规则：匹配前端请求的Origin，返回允许的域名（无匹配则返回空）
map$http_origin$allow_origin{
#白名单1：生产环境主域名（如PC端）
~^https?://www.your-domain.com$$http_origin;
#白名单2：移动端域名
~^https?://m.your-domain.com$$http_origin;
#白名单3：管理后台域名
~^https?://admin.your-domain.com$$http_origin;
#白名单4：支持端口（如测试环境的前端端口，生产建议统一80/443）
~^https?://test.your-domain.com:8080$$http_origin;
#默认值：非白名单域名返回空（浏览器会拦截跨域）
default"";
}

#2.可选：定义允许的请求头（复用变量，避免重复配置）
map$http_access_control_request_headers$allow_headers{
default"Content-Type,Authorization,Token,X-Requested-With";
}

#=====================第二步：配置Server块=====================
server{
listen443ssl;#生产环境建议强制HTTPS
server_nameapi.your-domain.com;#你的后端接口域名

#SSL配置（生产环境必加，省略证书配置示例）
ssl_certificate/etc/nginx/ssl/your-domain.crt;
ssl_certificate_key/etc/nginx/ssl/your-domain.key;

#匹配需要跨域的接口路径（如/api开头）
location/api/{
#=====================核心跨域配置=====================
#1.动态返回允许的Origin（来自上面的map变量）
add_headerAccess-Control-Allow-Origin$allow_originalways;
#2.允许携带Cookie/Token（生产环境必备）
add_headerAccess-Control-Allow-Credentialstruealways;
#3.允许的请求方法（覆盖所有常用方法）
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,PATCH,OPTIONS'always;
#4.允许的请求头（复用上面的变量）
add_headerAccess-Control-Allow-Headers$allow_headersalways;
#5.预检请求缓存时间（减少OPTIONS请求次数，优化性能）
add_headerAccess-Control-Max-Age86400always;

#6.处理OPTIONS预检请求（关键：直接返回204，不转发到后端）
if($request_method=OPTIONS){
return204;
}

#=====================反向代理配置=====================
#转发到后端真实服务地址（根据你的实际情况修改）
proxy_passhttp://127.0.0.1:8080;#后端服务IP+端口
#传递真实请求信息给后端（便于日志/鉴权）
proxy_set_headerHost$host;
proxy_set_headerX-Real-IP$remote_addr;
proxy_set_headerX-Forwarded-For$proxy_add_x_forwarded_for;
proxy_set_headerX-Forwarded-Proto$scheme;#传递HTTPS协议
}
}

#可选：HTTP强制跳转HTTPS（生产环境建议）
server{
listen80;
server_nameapi.your-domain.com;
return301https://$host$request_uri;
}
}
```

### 3、关键配置说明（生产环境必看）

3.1、`map`指令的位置：`map`必须定义在`http`块内、`server`块外部，否则Nginx会报语法错误。

3.2、域名匹配规则：`~^https?://www.your-domain.com$`中，`~`表示正则匹配，`^`/`$`强制完全匹配，`https?`兼容HTTP/HTTPS；避免模糊匹配（如只写`your-domain.com`），防止恶意域名利用子域名跨域。

3.3、`always`参数的必要性：不加`always`时，Nginx仅在200/204/301等成功响应中添加跨域头，404/500等错误响应会丢失跨域头，导致前端报错。

3.4、Cookie/Token适配：开启`Access-Control-Allow-Credentialstrue`后，`Access-Control-Allow-Origin`不能用`*`，必须是具体域名；前端请求需设置`withCredentials:true`（Axios/fetch均支持）。

3.5、性能优化：`Access-Control-Max-Age86400`表示预检请求的结果缓存24小时，避免浏览器频繁发送OPTIONS请求。

### 4、配置验证步骤

**检查语法**：

```bash
nginx-t
输出：nginx:configurationfile/etc/nginx/nginx.conftestissuccessful
表示语法正确。
```

**平滑重载配置**（不中断服务）：

```bash
nginx-sreload
```

测试跨域是否生效：

用`curl`模拟前端请求，验证响应头是否正确：

```bash
#模拟允许的域名请求
curl-XOPTIONS-H"Origin:https://www.your-domain.com"-Ihttps://api.your-domain.com/api/test
#响应头应包含：
Access-Control-Allow-Origin:https://www.your-domain.com
#模拟不允许的域名请求
curl-XOPTIONS-H"Origin:https://hack.com"-Ihttps://api.your-domain.com/api/test
#响应头无Access-Control-Allow-Origin浏览器会拦截
```

### 总结

1.生产环境多域名跨域的核心是通过`map`指令定义域名白名单，动态返回`Access-Control-Allow-Origin`；

2.必须开启`Access-Control-Allow-Credentials`并禁用`*`通配符，保证安全性；

3.处理OPTIONS预检请求、添加`always`参数、强制HTTPS是生产环境的必备配置。

## 第六节：多域名跨域+Nginx负载均衡（生产级）

该配置既能解决多域名跨域问题，又能将请求分发到多台后端服务器，提升服务的可用性和性能。以下是可直接复用的完整配置模板，并详细解释负载均衡核心逻辑。

### 一、核心配置思路

1. 先通过`upstream`指令定义后端服务器集群（负载均衡池）；

2. 复用之前的`map`指令实现多域名跨域白名单；

3. 在`location`块中同时配置跨域头和反向代理到负载均衡池；

4. 增加负载均衡的健康检查、权重分配等生产级配置。

### 二、完整配置示例（跨域+负载均衡）

```nginx
#=====================第一步：全局配置（http块内）=====================
http{
#1.定义后端服务器集群（负载均衡池）
upstreambackend_cluster{
#后端服务器1：权重1（权重越高，分配的请求越多）
server192.168.1.100:8080weight=1max_fails=3fail_timeout=30s;
#后端服务器2：权重2
server192.168.1.101:8080weight=2max_fails=3fail_timeout=30s;
#可选：后端服务器3（备用，只有当主服务器都不可用时才启用）
server192.168.1.102:8080backup;

#负载均衡策略（默认轮询，可选：ip_hash/least_conn/fair）
#ip_hash：按客户端IP哈希，保证同一客户端请求固定服务器（解决会话粘滞）
#least_conn：优先分配给连接数最少的服务器
ip_hash;

#健康检查相关（Nginx1.19+支持主动健康检查，需额外配置，这里是被动检查）
keepalive32;#保持与后端的长连接数量，提升性能
}

#2.多域名跨域白名单（复用之前的配置）
map$http_origin$allow_origin{
~^https?://www.your-domain.com$$http_origin;#PC端
~^https?://m.your-domain.com$$http_origin;#移动端
~^https?://admin.your-domain.com$$http_origin;#管理后台
default"";#非白名单域名拒绝跨域
}

#3.允许的请求头（复用变量）
map$http_access_control_request_headers$allow_headers{
default"Content-Type,Authorization,Token,X-Requested-With";
}

#=====================第二步：Server块配置=====================
server{
listen443ssl;
server_nameapi.your-domain.com;#接口域名

#SSL配置（生产环境必配）
ssl_certificate/etc/nginx/ssl/your-domain.crt;
ssl_certificate_key/etc/nginx/ssl/your-domain.key;
ssl_protocolsTLSv1.2TLSv1.3;#禁用低版本协议，提升安全性
ssl_prefer_server_cipherson;

#匹配接口路径
location/api/{
#=====================跨域配置（与之前一致）=====================
add_headerAccess-Control-Allow-Origin$allow_originalways;
add_headerAccess-Control-Allow-Credentialstruealways;
add_headerAccess-Control-Allow-Methods'GET,POST,PUT,DELETE,PATCH,OPTIONS'always;
add_headerAccess-Control-Allow-Headers$allow_headersalways;
add_headerAccess-Control-Max-Age86400always;

#处理OPTIONS预检请求
if($request_method=OPTIONS){
return204;
}

#=====================负载均衡+反向代理配置=====================
#代理到后端服务器集群（替代单个proxy_pass）
proxy_passhttp://backend_cluster;

#关键代理头配置（传递真实请求信息给后端）
proxy_set_headerHost$host;
proxy_set_headerX-Real-IP$remote_addr;
proxy_set_headerX-Forwarded-For$proxy_add_x_forwarded_for;
proxy_set_headerX-Forwarded-Proto$scheme;#传递HTTPS协议

#负载均衡优化配置
proxy_connect_timeout5s;#连接后端超时时间
proxy_send_timeout10s;#发送请求超时时间
proxy_read_timeout10s;#读取响应超时时间
proxy_bufferingon;#开启缓冲区，提升性能
proxy_buffer_size4k;#缓冲区大小
proxy_buffers432k;

#长连接配置（与upstream的keepalive配合）
proxy_http_version1.1;
proxy_set_headerConnection"";
}

#可选：静态资源路径（如果有后端静态资源）
location/static/{
proxy_passhttp://backend_cluster;
expires7d;#静态资源缓存7天，减轻后端压力
}
}

#HTTP强制跳转HTTPS
server{
listen80;
server_nameapi.your-domain.com;
return301https://$host$request_uri;
}
}
```

### 三、核心配置说明（负载均衡重点）

#### 1.`upstream`负载均衡池

- `server`：定义后端服务器地址，格式为`IP:端口`或`域名:端口`；

- `weight`：权重，示例中192.168.1.101权重为2，会接收2/3的请求，192.168.1.100接收1/3；

- `max_fails=3fail_timeout=30s`：如果某台服务器30秒内失败3次，标记为不可用，30秒后重试；

- `backup`：备用服务器，只有当所有非备用服务器都不可用时才会被启用；

- `ip_hash`：按客户端IP哈希分配，解决「会话粘滞」问题（比如用户登录态只存在某台服务器上），如果后端是无状态服务（如微服务），可改用默认的`round_robin`（轮询）或`least_conn`（最少连接）。

#### 2.负载均衡策略选择

|策略|适用场景|
|---|---|
|`round_robin`（默认）|无状态服务，所有服务器性能相近|
|`ip_hash`|有状态服务（如会话存储），需固定客户端到服务器|
|`least_conn`|服务器性能差异大，优先分配给连接少的服务器|
|`fair`|按后端响应时间分配，需编译第三方模块|
#### 3.健康检查补充

上面的配置是「被动健康检查」（只有请求失败才标记服务器不可用），如果你的Nginx版本≥1.19.0，可开启「主动健康检查」（Nginx主动探测后端状态），添加以下配置到`upstream`块：

```nginx

upstreambackend_cluster{
#原有配置...
zonebackend_zone64k;#必须定义zone才能开启主动健康检查
health_checkinterval=5stimeout=1spasses=2fails=2;#每5秒检查，超时1秒，2次成功恢复，2次失败标记不可用
}
```

### 四、配置验证与维护

1. **验证配置语法**：
    `nginx-t`

2. **平滑重载配置**：
    `nginx-sreload`

3. **查看负载均衡状态（可选）**：如需可视化查看后端服务器状态，可安装nginx-module-vts模块，或通过Nginx日志分析：
    `#查看请求分发情况
    tail-f/var/log/nginx/access.log|grepbackend_cluster`

### 总结

1. 生产环境跨域+负载均衡的核心是：用`upstream`定义后端集群，`proxy_pass`指向集群名称，同时保留多域名跨域的`map`配置；

2. 负载均衡策略需根据后端服务是否有状态选择（`ip_hash`用于有状态，`round_robin/least_conn`用于无状态）；

3. 配置`max_fails/fail_timeout`和`backup`服务器，提升服务的容灾能力；

4. 生产环境建议开启HTTPS，并配置合理的超时时间和缓存策略。
> （注：文档部分内容可能由AI生成）