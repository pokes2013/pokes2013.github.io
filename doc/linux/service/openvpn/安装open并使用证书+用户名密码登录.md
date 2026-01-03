#  安装openVPN并使用证书+用户名密码登录



openvpn是一个vpn工具,用于创建虚拟专用网络(Virtual Private Network)加密通道的免费开源软件,提供证书验证功能,也支持用户名密码认证登录方式,当然也支持两者合一,为服务器登录和连接提供更加安全的方式,可以在不同网络访问场所之间搭建类似于局域网的专用网络通道,配合特定的代理服务器,可用于访问特定受限网站(你懂得)或者突破内部网络限制.



## 安装v

模拟运行环境:centos6系列系统



```
# 关闭selinux
setenforce 0
sed -i '/^SELINUX=/c\SELINUX=disabled' /etc/selinux/config
#把官方源备份整理,然后摒弃
cd /etc/yum.repos.d/
mkdir yum.bak
mv CentOS-* yum.bak/
# 安装epel源,因为资源比较全
#这是6系列系统的源
rpm -Uvh http://mirrors.kernel.org/fedora-epel/6/i386/epel-release-6-8.noarch.rpm 
#这是7系列系统的源
#rpm -Uvh http://mirrors.kernel.org/fedora-epel/7Server/x86_64/e/epel-release-7-8.noarch.rpm
#安装163源,和epel互补,速度也较快
#这是6系列系统的源
wget http://mirrors.163.com/.help/CentOS6-Base-163.repo
#这是7系列系统的源 
#wget http://mirrors.163.com/.help/CentOS7-Base-163.repo 
yum makecache
# 安装openssl和lzo，lzo用于压缩通讯数据加快传输速度
yum -y install openssl openssl-devel lzo
# 安装openvpn和easy-rsa
yum -y install openvpn easy-rsa
```

其实也可以源码编译,不过费时费力,倒是效果一样,而且版本不同并不影响太多功能,内部系统要求也不至于那么高,所以直接yum安装也是够用的了.

## 配置

一般来说,openvpn需要配置证书来使用,假如你只使用用户名密码来认证登录,也不是不可以,只是安全性稍微打了一些折扣,下面来看看配证书.
先找到制作证书的工具easy-rsa存放的位置,一般yum安装的软件大多数都是这个路径/usr/share



```
#先确认位置
find / -name easy-rsa
/usr/share/easy-rsa
/usr/share/doc/easy-rsa
#修改vars文件
cd /usr/share/easy-rsa/
vim vars
#修改注册信息，比如公司地址、公司名称、部门名称等。
export KEY_COUNTRY="CN"
export KEY_PROVINCE="GD"
export KEY_CITY="canton"
export KEY_ORG="XXX.com"
export KEY_EMAIL="admin@xxx.com"
export KEY_OU="XXX.com"
#保存退出,然后加载一下,注意当前文件夹路径,后续操作暂时不能更换文件夹路径,不然会报错
source vars
# 清除keys目录下所有与证书相关的文件
# 下面步骤生成的证书和密钥都在/usr/share/easy-rsa/keys目录里
./clean-all
# 生成根证书ca.crt和根密钥ca.key（一路按回车即可）
./build-ca
# 为服务端生成证书和私钥（一路按回车，直到提示需要输入y/n时，输入y再按回车，一共两次）
./build-key-server server
# 每一个登陆的×××客户端需要有一个证书，每个证书在同一时刻只能供一个客户端连接，下面建立2份
# 为客户端生成证书和私钥（一路按回车，直到提示需要输入y/n时，输入y再按回车，一共两次）
./build-key test1
./build-key test2
# 创建迪菲·赫尔曼密钥，会生成dh2048.pem文件（生成过程比较慢，在此期间不要去中断它）
./build-dh
# 生成ta.key文件（防DDosvpn、UDP淹没等恶意vpn）
openvpn --genkey --secret keys/ta.key
```



证书已经生成完毕了,来看看证书存放的目录keys,就在当前文件夹目录里面(所以叫你别换文件夹路径)

```
ll keys/
total 96
-rw-r--r-- 1 root root 5551 Oct 25 17:18 01.pem
-rw-r--r-- 1 root root 5444 Oct 25 17:19 02.pem
-rw-r--r-- 1 root root 1708 Oct 25 17:17 ca.crt
-rw------- 1 root root 1704 Oct 25 17:17 ca.key
-rw-r--r-- 1 root root  424 Oct 25 17:20 dh2048.pem
-rw-r--r-- 1 root root 5444 Oct 25 17:19 test1.crt
-rw-r--r-- 1 root root 1074 Oct 25 17:18 test1.csr
-rw------- 1 root root 1704 Oct 25 17:18 test1.key
-rw-r--r-- 1 root root 5444 Oct 25 17:19 test2.crt
-rw-r--r-- 1 root root 1074 Oct 25 17:18 test2.csr
-rw------- 1 root root 1704 Oct 25 17:18 test2.key
-rw-r--r-- 1 root root  259 Oct 25 17:19 index.txt
-rw-r--r-- 1 root root   21 Oct 25 17:19 index.txt.attr
-rw-r--r-- 1 root root   21 Oct 25 17:18 index.txt.attr.old
-rw-r--r-- 1 root root  128 Oct 25 17:18 index.txt.old
-rw-r--r-- 1 root root    3 Oct 25 17:19 serial
-rw-r--r-- 1 root root    3 Oct 25 17:18 serial.old
-rw-r--r-- 1 root root 5551 Oct 25 17:18 server.crt
-rw-r--r-- 1 root root 1070 Oct 25 17:18 server.csr
-rw------- 1 root root 1704 Oct 25 17:18 server.key
-rw------- 1 root root  636 Oct 25 17:23 ta.key
```

好了,证书准备完毕,就开始正式配置服务端了,要定义配置文件

```
#在openvpn的配置目录下新建一个keys目录
mkdir /etc/openvpn/keys
# 将需要用到的openvpn证书和密钥复制一份到刚创建好的keys目录中
cp /usr/share/easy-rsa/keys/* /etc/openvpn/keys/
#编辑server.conf,有些版本有模板,有些版本没有,只能自建
vim /etc/openvpn/server.conf
#定义端口号,默认是1194,不想被"特殊照顾",那就改一下吧
port 11194
# 改成tcp，默认使用udp，如果使用HTTP Proxy，必须使用tcp协议
proto tcp
#路由模式，桥接模式用dev tap
dev tun 
# 路径前面加keys，全路径为/etc/openvpn/keys/ca.crt
ca keys/ca.crt
cert keys/server.crt
key keys/server.key  # This file should be kept secret
dh keys/dh2048.pem
#默认虚拟局域网网段，不要和实际的局域网冲突即可,server是路由模式，桥接模式用server-bridge
server 10.8.0.0 255.255.255.0 
ifconfig-pool-persist ipp.txt
#指定×××能访问的网络地址,10.0.0.0/8是我这台×××服务器所在的内网的网段，按实际内网地址设置
push "route 10.0.0.0 255.0.0.0"
#限制vpn只在访问某个ip时使用,其他网络访问不使用vpn,按需求设置
#push "route 118.184.180.46 255.255.255.255"
# 可以让客户端之间相互访问直接通过openvpn程序转发，根据需要设置
client-to-client
# 如果客户端都使用相同的证书和密钥连接×××，一定要打开这个选项，否则每个证书只允许一个人连接×××
duplicate-cn
keepalive 10 120
tls-auth keys/ta.key 0 # This file is secret
comp-lzo
persist-key
persist-tun
# Open×××的状态日志，默认为/etc/openvpn/openvpn-status.log
status openvpn-status.log
# Open×××的运行日志，默认为/etc/openvpn/openvpn.log 
log-append openvpn.log
#日志等级,看你需求,5就看多一些调试信息,3就简单些
verb 3
###--加入脚本处理，如用密码验证
script-security 3 
###指定只用的认证脚本
auth-user-pass-verify /etc/openvpn/checkpsw.sh via-env 
###不请求客户的CA证书，使用User/Pass验证，如果同时启用证书和密码认证，注释掉该行
#client-cert-not-required 
### 使用客户提供的UserName作为Common Name
username-as-common-name 
#保存退出,其他配置请看最后列出的配置说明
```

然后就是密码认证的脚本了,需要自己创建,放在openvpn的控制目录,和keys文件夹同一个文件夹(不是放keys里面)就可以了,server.conf配置文件里可以体现.

```
#先看看脚本
cat /etc/openvpn/checkpsw.sh
#!/bin/sh
###########################################################
# checkpsw.sh (C) 2004 Mathias Sundman <mathias@openvpn.se>
#
# This script will authenticate Open××× users against
# a plain text file. The passfile should simply contain
# one row per user with the username first followed by
# one or more space(s) or tab(s) and then the password.
PASSFILE="/etc/openvpn/psw-file"
LOG_FILE="/var/log/openvpn-password.log"
TIME_STAMP=`date "+%Y-%m-%d %T"`
###########################################################
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

#当然了,还要建议个记录用户名和密码的文件,脚本标记的文件是psw-file,前面是用户名.空格后是密码
cat /etc/openvpn/psw-file
admin admin1234
```

配置写完了,最后来看看系统还要做一些东西

```
#开启路由转发功能,在/etc/sysctl.conf里添加更改
sed -i '/net\.ipv4\.ip\_forward/c\net\.ipv4\.ip\_forward\=1' /etc/sysctl.conf
#有些可能没有这个设置,那就在这个文件最后加入
echo "net\.ipv4\.ip\_forward\=1" >>  /etc/sysctl.conf
#重载一下这个文件的参数
sysctl -p
# 配置防火墙，别忘记保存
iptables -I INPUT -p tcp --dport 11194 -m comment --comment "openvpn" -j ACCEPT
iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -j MASQUERADE
service iptables save
#启动openvpn并设置为开机启动
service openvpn start
chkconfig openvpn on
```

不要以为完成了,还有客户端的配置文件要搞一下,这个配置文件是要放到客户端上面去的.

```
# 编辑client.ovpn,也是有些版本有模板,有些版本没有,只能自建
vim client.ovpn
client
# 路由模式
dev tun 
# 改为tcp
proto tcp
# Open×××服务器的外网IP和端口
remote 121.95.16.xxx 11194
resolv-retry infinite
nobind
persist-key
persist-tun
ca ca.crt
# test1的证书
cert test1.crt
# test1的密钥
key test1.key
ns-cert-type server
tls-auth ta.key 1
comp-lzo
verb 3
#密码认证相关
auth-user-pass
```

最后,准备客户端的配置文件

```
#先创建一个config文件夹,
mkdir config 
#将刚刚编辑好的client.o***和keys文件夹里面的ca.crt、test1.crt、test1.key、ta.key拷贝进去.
cp -ar client.o*** config/
cd keys
cp -ar  ca.crt test1.crt test1.key ta.key config/
#压缩
tar zcf config.tar.gz config
```

 最后把config.tar.gz拷贝出来备用,最后在客户端里面使用 