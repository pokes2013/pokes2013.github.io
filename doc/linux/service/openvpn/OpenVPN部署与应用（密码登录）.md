# OpenVPN部署与应用（密码登录）

### 简介

------

VPN直译就是虚拟专用通道，是提供给企业之间或者个人与公司之间安全数据传输的隧道，OpenVPN无疑是Linux下开源VPN的先锋，提供了良好的性能和友好的用户GUI。

OpenVPN大量使用了OpenSSL加密库中的SSLv3/TLSv1协议函数库。

OpenVPN 是一个基于 OpenSSL 库的应用层 VPN 实现。和传统 VPN 相比，它的优点是简单易用。

 

### 1.环境规划

------

| 主机名   | 外网IP        | 内网IP      | 角色          |
| -------- | ------------- | ----------- | ------------- |
| openvpn  | 10.0.0.61     | 172.16.1.61 | OpenVPN服务端 |
| web01    | 172.16.1.7    | 内网主机    |               |
| web02    | 172.16.1.8    | 内网主机    |               |
| 10.0.0.1 | OpenVPN客户端 |             |               |

 

### 2.生成证书

------

#### 2.1下载证书生成工具`easy-rsa`

```bash
yum -y install easy-rsa
```

#### 2.2 创建证书环境目录

```bash
mkdir -p /opt/easy-rsa
cp -a /usr/share/easy-rsa/3.0.7/* /opt/easy-rsa/
cp -a /usr/share/doc/easy-rsa-3.0.7/vars.example /opt/easy-rsa/vars
```

#### 2.3 生成秘钥前，准备`vars`文件

修改文件`/opt/easy-rsa/vars`中的如下配置（要取消注释）

```bash
set_var EASYRSA_DN      "cn_only"
set_var EASYRSA_REQ_COUNTRY     "CN"
set_var EASYRSA_REQ_PROVINCE    "Shanghai"
set_var EASYRSA_REQ_CITY        "Shanghai"
set_var EASYRSA_REQ_ORG         "whb"
set_var EASYRSA_REQ_EMAIL       "whb@qq.com"
set_var EASYRSA_NS_SUPPORT      "yes"
```

#### 2.4 初始化

在当前目录下创建`pki`目录，用于存储证书

```bash
cd /opt/easy-rsa/
/opt/easy-rsa/easyrsa init-pki
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-1.png)

#### 2.5 创建根证书

根证书用于ca对之后生成的server和client证书签名时使用。

```bash
/opt/easy-rsa/easyrsa build-ca
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-2.png)

#### 2.6 创建server端证书和私钥文件

nopass表示不加密私钥文件，生成过程中直接回车默认

```bash
/opt/easy-rsa/easyrsa gen-req server nopass
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-3.png)

#### 2.7 给server证书签名

```bash
/opt/easy-rsa/easyrsa sign server server
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-4.png)

#### 2.8 创建Diffie-Hellman文件，秘钥交换时的Diffie-Hellman算法

```bash
/opt/easy-rsa/easyrsa gen-dh
```

#### 2.9 创建server端证书和私钥文件

nopass表示不加密私钥文件，生成过程中直接回车默认

```bash
/opt/easy-rsa/easyrsa gen-req client nopass
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-5.png)

#### 2.10 给client端证书签名

```bash
/opt/easy-rsa/easyrsa sign client client
```

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-6.png)

 

### 3.OpenVPN服务端部署

------

#### 3.1 安装`openvpn`软件

```bash
yum -y install openvpn 
```

#### 3.2 修改配置文件

自行创建配置文件`/etc/openvpn/server.conf`，并加入如下配置

```bash
[root@openvpn ~]# cat /etc/openvpn/server.conf
port 1194 #端口
proto udp #协议
dev tun #采用路由隧道模式tun
ca ca.crt #ca证书文件位置
cert server.crt #服务端公钥名称
key server.key #服务端私钥名称
dh dh.pem #交换证书
server 10.8.0.0 255.255.255.0 #给客户端分配地址池，注意：不能和VPN服务器内网网段有相同
push "route 172.16.1.0 255.255.255.0" #允许客户端访问内网172.16.1.0网段
ifconfig-pool-persist ipp.txt #地址池记录文件位置
keepalive 10 120 #存活时间，10秒ping一次,120 如未收到响应则视为断线
max-clients 100 #最多允许100个客户端连接
status openvpn-status.log #日志记录位置
verb 3 #openvpn版本
client-to-client #客户端与客户端之间支持通信
log /var/log/openvpn.log #openvpn日志记录位置
persist-key #通过keepalive检测超时后，重新启动VPN，不重新读取keys，保留第一次使用的keys。
persist-tun #检测超时后，重新启动VPN，一直保持tun是linkup的。否则网络会先linkdown然后再linkup
duplicate-cn
```

#### 3.3 拷贝证书到openvpn主配置文件目录下

```bash
cp -a /opt/easy-rsa/pki/ca.crt /etc/openvpn/
cp -a /opt/easy-rsa/pki/issued/server.crt /etc/openvpn/
cp -a /opt/easy-rsa/pki/private/server.key /etc/openvpn/
cp -a /opt/easy-rsa/pki/dh.pem /etc/openvpn/
```

#### 3.4 启动openvpn

```bash
systemctl -f enable openvpn@server.service
systemctl start openvpn@server.service
```

 

### 4.OpenVPN客户端部署

------

#### 4.1 安装OpenVPN客户端软件

这里是在windows环境下部署OpenVPN的客户端的，首先需要下载安装OpenVPN客户端软件

#### 4.2 配置客户端

拷贝服务端生成的证书到OpenVPN安装目录的`config`目录下

分别拷贝以下几个文件

```bash
/opt/easy-rsa/pki/ca.crt 
/opt/easy-rsa/pki/issued/client.crt
/opt/easy-rsa/pki/private/client.key
```

#### 4.3 编写客户端配置文件

在OpenVPN安装目录的`config`目录下，新建一个`client.ovpn`文件，在文件中添加如下配置：

```bash
client #指定当前VPN是客户端
dev tun #使用tun隧道传输协议
proto udp #使用udp协议传输数据
remote 10.0.0.61 1194 #openvpn服务器IP地址端口号
resolv-retry infinite #断线自动重新连接，在网络不稳定的情况下非常有用
nobind #不绑定本地特定的端口号
ca ca.crt #指定CA证书的文件路径
cert client.crt #指定当前客户端的证书文件路径
key client.key #指定当前客户端的私钥文件路径
verb 3 #指定日志文件的记录详细级别，可选0-9，等级越高日志内容越详细
persist-key #通过keepalive检测超时后，重新启动VPN，不重新读取keys，保留第一次使用的keys
persist-tun #检测超时后，重新启动VPN，一直保持tun是linkup的。否则网络会先linkdown然后再linkup
```

#### 4.4 启动OpenVPN客户端软件

双击安装好后的OpenVPN软件，然后右键点击连接。

连接成功后，在托任务栏位置的OpenVPN图标会变绿色，则说明OpenVPN已经连接成功。

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-7.png)

OpenVPN会分配一个IP地址给客户端，客户端会使用该虚拟网络IP地址与服务端进行通信。

 

### 5.OpenVPN客户端访问内网

------

#### 5.1 在OpenVPN服务端开启内核转发

无论用哪种方式访问内部网络，都必须开启内核转发。

```bash
[root@openvpn ~]# echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
```

#### 5.2 添加路由规则方式访问内部网络

在内网主机web01上添加一条路由规则，让web01有回到OpenVPN客户端的路由。如果不添加，那web01只能接受到来自客户端的包，但是没法把响应的包传回去。

弊端：如果有成白上千台主机时，每一台主机都要添加路由规则，这样任务量是比较大的。

```bash
[root@web01 ~]# route add -net 10.8.0.0/24 gw 172.16.1.61
```

#### 5.3 添加防火墙方式访问内部网络

在服务端开启防火墙，放行openvpn服务，并且开启`masquerade`。

优点：只需在OpenVPN服务端配置防火墙规则，内部网络主机无需配置。

```bash
systemctl start firewalld
firewall-cmd --add-masquerade --permanent
firewall-cmd --add-service=openvpn --permanent
firewall-cmd --reload
```

 

### 6.双重验证登录

------

#### 6.1 修改server端配置

- 修改配置文件

在配置文件`/etc/openvpn/server.conf`中添加以下配置

```bash
script-security 3              #允许使用自定义脚本
auth-user-pass-verify /etc/openvpn/check.sh via-env
username-as-common-name         #用户密码登陆方式验证
```

注意：如果加上`client-cert-not-required`则代表只使用用户名密码方式验证登录，如果不加，则代表需要证书和用户名密码双重验证登录！

#### 6.2 添加脚本

```bash
[root@openvpn ~]# vim /etc/openvpn/check.sh
#!/bin/sh
###########################################################
PASSFILE="/etc/openvpn/openvpnfile"
LOG_FILE="/var/log/openvpn-password.log"
TIME_STAMP=`date "+%Y-%m-%d %T"`

if [ ! -r "${PASSFILE}" ]; then
    echo "${TIME_STAMP}: Could not open password file \"${PASSFILE}\" for reading." >> ${LOG_FILE}
    exit 1
fi

CORRECT_PASSWORD=`awk '!/^;/&&!/^#/&&$1=="'${username}'"{print $2;exit}' ${PASSFILE}`

if [ "${CORRECT_PASSWORD}" = "" ]; then
    echo "${TIME_STAMP}: User does not exist: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
    exit 1
fi
if [ "${password}" = "${CORRECT_PASSWORD}" ]; then
    echo "${TIME_STAMP}: Successful authentication: username=\"${username}\"." >> ${LOG_FILE}
    exit 0
fi

echo "${TIME_STAMP}: Incorrect password: username=\"${username}\", password=\"${password}\"." >> ${LOG_FILE}
exit 1
```

给脚本添加执行权限

```bash
chmod +x /etc/openvpn/check.sh 
```

#### 6.3 编写用户密码文件

```bash
[root@openvpn ~]# cat /etc/openvpn/openvpnfile
whb 123456
```

#### 6.4 重启openvpn服务

```bash
systemctl restart openvpn@server.service
```

#### 6.5 修改客户端配置

在安装目录下`config`目录下的client.ovpn文件中添加如下配置

```bash
auth-user-pass
```

然后重启OpenVPN客户端软件。

再次使用就会跳出用户登录窗口了

![img](https://www.wanhebin.com/wp-content/uploads/2020/06/openvpn-8.png)

输入用户名和密码后登录成功。