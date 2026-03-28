

# ubuntu server安装docker



## 安装docker

```bash
sudo apt-get install docker  -y
docker --version
sudo systemctl start docker
sudo systemctl enable docker
```



## 一键配置 Docker Daemon

```bash
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<EOF
{
    "registry-mirrors": [
    "https://docker.1ms.run",
    "https://dytt.online",
    "https://docker-0.unsee.tech",
    "https://lispy.org",
    "https://docker.xiaogenban1993.com",
    "https://666860.xyz",
    "https://hub.rat.dev",
    "https://docker.m.daocloud.io",
    "https://demo.52013120.xyz",
    "https://proxy.vvvv.ee",
    "https://registry.cyou",
    "https://mirror.ccs.tencentyun.com",
    "https://docker.1panel.live"
    ]
}
EOF

sudo systemctl daemon-reload
sudo systemctl restart docker
```

## 每次加sudo很烦，将当前用户加入到docker组内

```bash
sudo usermod -aG docker pokes
```

## 完事之后拉去一个试试：

```bash
docker pull nginx:latest
```



## 安装docker-compose

```bash
sudo apt-get install docker-compose -y
sudo docker-compose --version
```

## 测试使用docker-compose部署一个简单的nginx

```bash
mkdir nginx-docker && cd nginx-docker
vim docker-compose.yml
```

添加内容

```bash
version: '3.8'

services:
  nginx:
    image: nginx:latest
    container_name: my-nginx
    ports:
      - "80:80"
```



一定要进入nginx-docker目录内执行

```bash
docker-compose up -d

暂停服务：docker-compose stop
停止服务：docker-compose down  //慎用：停止并移除容器、网络
查看日志：docker-compose logs
重启服务：docker-compose restart
检测配置文件是否有错误：docker-compose config -q
查看网络：docker network ls
```

可以成功访问。但是没有数据持久化.

接下来我们再试一个

```bash
mkdir nginx-ceshi2
vim docker-compose.yml
```

添加以下内容：

```bash
version: '3.1'
services:
  nginx:
    restart: always
    image: nginx
    container_name: nginx
    ports:
      - 5082:80
    volumes:
      - /home/pokes111/docker_nginx/conf.d/:/etc/nginx/conf.d
      - /home/pokes111/docker_nginx/html:/usr/share/nginx/html
      - /home/pokes111/docker_nginx/logs:/var/log/nginx
```

直接启动

```bash
docker-compose up -d
```

貌似启动成功，但是测试页无法访问！问题处在了哪里？

使用docker-compose logs命令查看日志，说是没有配置文件。

突然想起来，这样挂载宿主机目录，需要提前准备好Nginx.conf的配置文件和网页的index.html

配置文件：`vim /home/pokes111/docker_nginx/conf.d/nginx.cof`

```bash
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

index.html文件：`vim /home/pokes111/docker_nginx/html/index.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome to Nginx!</title>
</head>
<body>
    <h1>Welcome to Nginx!</h1>
    <p>If you see this page, the nginx web server is successfully installed and working.</p>
</body>
</html>
```

但是在生产中一般是将挂载目录和docker-compose.yml文件放到一个目录内，这样方便编辑切换目录准备配置文件等操作。

```bash
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    container_name: my-nginx
    ports:
      - "80:80"
    volumes:
      # 挂载自定义配置文件
      - ./conf:/etc/nginx/conf.d
      # 挂载网站静态资源
      - ./html:/usr/share/nginx/html
      # 挂载日志文件
      - ./logs:/var/log/nginx
    restart: unless-stopped
```

## 处理xshell粘贴长文本缩进混乱的问题

```bash
:set paste      // 设置不自动换行
 
然后按“shift+i”进入编辑模式，然后按“shift+insert”粘贴文本
 
:set nopaste    // 恢复默认设置
```



## Nginx配置文件解析

```bash
# 定义HTTP服务器块
server {
    # 监听IPv4端口80（HTTP默认端口）
    listen       80;
    # 监听IPv6端口80
    listen  [::]:80;
    # 服务器名称，localhost表示本地访问
    server_name  localhost;

    # 访问日志配置（当前被注释掉）
    #access_log  /var/log/nginx/host.access.log  main;

    # 处理根路径/的请求
    location / {
        # 网站根目录路径
        root   /usr/share/nginx/html;
        # 默认索引文件，按顺序查找
        index  index.html index.htm;
    }

    # 自定义404错误页面（当前被注释掉）
    #error_page  404              /404.html;

    # 配置服务器错误页面的重定向
    # 当出现500、502、503、504错误时，显示/50x.html
    error_page   500 502 503 504  /50x.html;
    
    # 精确匹配/50x.html路径
    location = /50x.html {
        # 错误页面所在目录
        root   /usr/share/nginx/html;
    }
}
```

