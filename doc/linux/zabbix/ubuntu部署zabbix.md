### Ubuntu Noble 部署 Zabbix 6.4 笔记（适配 PHP 8.0+）



开始之前先说明几个问题：

> 1、ubuntu版本的问题：
>
> - ubuntu22.04LTS,Jammy
>
> - ubuntu24.04LTS,Noble（本文）
>
> 2、zabbi和php版本兼容的问题：
>
> - zabbix6.4不兼容php7.4
>
> - zabbix6.1,最低php7.4-最高8.0
>
> - zabbix6.4,最低php8.0-最高8.2（本文）
>
> - zabbix7.1,最低php8.1

#### 一、部署前环境准备（基于 LAMP 架构）

##### 1. 更新系统源与系统包

```bash
# 编辑源配置文件
sudo vim /etc/apt/sources.list

# 添加阿里云/清华源（Noble 版本）
deb http://mirrors.aliyun.com/ubuntu/ noble main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ noble-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ noble-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ noble-backports main restricted universe multiverse

deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-security main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ noble-backports main restricted universe multiverse

# 更新源并升级系统
sudo apt update && sudo apt upgrade -y

# 安装基础依赖
sudo apt install -y wget curl software-properties-common
```

##### 2. 安装 MariaDB（数据库）

```bash
# 安装 MariaDB 服务
sudo apt install -y mariadb-server mariadb-client

# 安全初始化（设置 root 密码、移除匿名用户等）
sudo mysql_secure_installation
```

- 按提示输入 `Y` 并设置 root 密码（后续需使用）
- 依次确认移除匿名用户、禁止 root 远程登录、删除 test 数据库、刷新权限

##### 3. 安装 Apache 和 PHP 8.0+（Ubuntu Noble 默认 PHP 版本兼容）

```bash
# 安装 Apache 服务
sudo apt install -y apache2

# 安装 PHP 及 Zabbix 必需扩展（Noble 自带 PHP 8.1+，满足 8.0+ 要求）
sudo apt install -y php php-mysql php-gd php-bcmath php-mbstring \
php-xml php-zip php-ldap php-json php-curl libapache2-mod-php

# 重启 Apache 使 PHP 生效
sudo systemctl restart apache2
```

#### 二、安装 Zabbix 6.4 服务端

##### 1. 添加 Zabbix 官方源

```bash
# 下载 Zabbix 6.4 源配置（适配 Ubuntu 22.04，Noble 兼容）
wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb

# 安装源
sudo dpkg -i zabbix-release_6.4-1+ubuntu22.04_all.deb

# 更新源缓存
sudo apt update
```

##### 2. 创建 Zabbix 数据库

```sql
# 登录 MariaDB（输入 root 密码）
sudo mysql -u root -p

# 执行 SQL 命令（逐行输入）
CREATE DATABASE zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER zabbix@localhost IDENTIFIED BY '自定义密码';  # 替换为实际密码
GRANT ALL PRIVILEGES ON zabbix.* TO zabbix@localhost;
FLUSH PRIVILEGES;
EXIT;
```

##### 3. 导入 Zabbix 初始数据库

```bash
# 安装 Zabbix 数据库工具
sudo apt install -y zabbix-sql-scripts zabbix-server-mysql

# 导入初始数据（输入上述创建的 zabbix 用户密码）
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -u zabbix -p zabbix
```

##### 4. 配置 Zabbix Server

```bash
# 编辑配置文件
sudo nano /etc/zabbix/zabbix_server.conf
```

修改以下参数（其他默认）：

```ini
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=你的数据库密码  # 替换为实际设置的密码
```

保存退出（`Ctrl+O` → 回车 → `Ctrl+X`）

##### 5. 安装 Zabbix Web 前端

```bash
# 安装 Web 组件及 Apache 配置
sudo apt install -y zabbix-frontend-php zabbix-apache-conf

# 配置 PHP 时区（关键，避免 Web 界面报错）
sudo nano /etc/php/8.1/apache2/php.ini  # 注意：Noble 可能为 php/8.2 等，需根据实际版本调整路径
```

修改时区参数：

```ini
date.timezone = Asia/Shanghai
```

重启 Apache：

```bash
sudo systemctl restart apache2
```

##### 6. 启动 Zabbix 服务并设置自启

```bash
# 启动服务端
sudo systemctl start zabbix-server

# 设置开机自启
sudo systemctl enable zabbix-server

# 检查服务状态（确保显示 active (running)）
sudo systemctl status zabbix-server
```

#### 三、Web 界面初始化配置

1. 浏览器访问：`http://服务器IP/zabbix`
2. 按向导配置：
   - 步骤 1：确认环境检查通过（PHP 版本需 ≥8.0）
   - 步骤 2：填写数据库信息（密码为 zabbix 用户密码）
   - 步骤 3：自定义 Zabbix 服务器名称（如 “Noble-Zabbix”）
   - 步骤 4：确认配置并完成安装
3. 登录默认账号：
   - 用户名：`Admin`
   - 密码：`zabbix`（建议登录后立即修改）

#### 四、添加 Ubuntu 客户端监控

1. **客户端安装 Zabbix Agent**：

```bash
# 添加 Zabbix 源（同服务端）
wget https://repo.zabbix.com/zabbix/6.4/ubuntu/pool/main/z/zabbix-release/zabbix-release_6.4-1+ubuntu22.04_all.deb
sudo dpkg -i zabbix-release_6.4-1+ubuntu22.04_all.deb
sudo apt update

# 安装 Agent
sudo apt install -y zabbix-agent

# 配置 Agent
sudo nano /etc/zabbix/zabbix_agentd.conf
```

修改核心参数：

```ini
Server=Zabbix服务端IP  # 允许连接的服务端IP
ServerActive=Zabbix服务端IP  # 主动上报的服务端IP
Hostname=客户端主机名  # 需与Web界面添加的主机名一致
```

1. **启动 Agent**：

```bash
sudo systemctl start zabbix-agent
sudo systemctl enable zabbix-agent
```

1. **Web 界面添加主机**：
   - 进入「配置」→「主机」→「创建主机」
   - 填写主机名（与 Agent 配置一致）、可见名称、所属群组
   - 「接口」添加客户端 IP，端口默认 10050
   - 「模板」链接 `Template OS Linux` 模板
   - 保存后几分钟即可在「监测」→「最新数据」查看监控项

#### 关键说明

- 适配 Ubuntu Noble 版本，使用系统自带 PHP 8.1+（满足 Zabbix 6.4 对 PHP ≥8.0 的要求）
- 核心步骤：LAMP 环境搭建 → 数据库配置 → Zabbix 服务部署 → 客户端接入
- 注意 PHP 时区配置和数据库密码一致性，否则会导致服务启动或 Web 界面异常





如果安装完仅有英文，其他语言都是灰色，可以参考这一片：

https://blog.csdn.net/qq_51688785/article/details/140154083