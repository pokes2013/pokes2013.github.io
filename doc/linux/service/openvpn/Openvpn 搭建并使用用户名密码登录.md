



# Openvpn 搭建并使用用户名密码登录



## 搭建前准备



Centos6.9 操作系统
[端口映射](https://so.csdn.net/so/search?q=端口映射&spm=1001.2101.3001.7020)设备（路由器 / 防火墙）



## 一、服务端搭建过程



### 1、安装 openvpn 和证书生成程序



[yum](https://so.csdn.net/so/search?q=yum&spm=1001.2101.3001.7020) -y install epel-release
yum -y install openvpn easy-[rsa](https://so.csdn.net/so/search?q=rsa&spm=1001.2101.3001.7020)



### 2、将 openvpn 的实例配置文件拷贝到 / etc/openvpn 下



cp /usr/share/doc/openvpn-2.4.11/sample/sample-config-files/server.conf /etc/openvpn/
cp /usr/share/doc/easy-rsa-3.0.8/vars.example /etc/openvpn/vars
cp -rf /usr/share/easy-rsa/3.0.8/* /etc/openvpn/



### 3、生成证书和秘钥



./easyrsa init-pki
./easyrsa build-ca nopass
./easyrsa gen-dh
./easyrsa build-server-full server nopass
./easyrsa build-client-full client nopass



### 4、修改 openvpn 配置文件



[root@openVPN issued]# cat /etc/openvpn/server.conf | grep -v ‘^#’ | grep -v ‘^$’
local 1.70.11.11
port 1194
proto tcp
dev tun
ca /etc/openvpn/pki/ca.crt
cert /etc/openvpn/pki/issued/server.crt
key /etc/openvpn/pki/private/server.key # This file should be kept secret
dh /etc/openvpn/pki/dh.pem
server 172.16.0.0 255.255.255.0
ifconfig-pool-persist ipp.txt
push “redirect-gateway def1 bypass-dhcp”
push “dhcp-option DNS 208.67.222.222”
client-to-client
duplicate-cn
keepalive 10 120
cipher AES-256-CBC
compress lz4-v2
push “compress lz4-v2”
user nobody
group nobody
persist-key
persist-tun
status /var/log/openvpn-status.log
log /var/log/openvpn.log
log-append openvpn.log
verb 7
explicit-exit-notify 0



## 二、客户端配置



### 1、下载客户端



客户端可以在官网下载，也可联系我通过阿里云盘分享



### 2、拷贝证书文件到客户端



/etc/easy-rsa/pki/private/client.key
/etc/easy-rsa/pki/issued/client.crt
/etc/easy-rsa/pki/ca.crt



将这三个文件拷贝至 openvpn 的安装目录中，然后增加 client.opven 文件，配置如下：



client
dev tun
proto tcp
sndbuf 0
rcvbuf 0
remote 1.70.11.11 1194
resolv-retry infinite
link-mtu 65500
persist-key
persist-tun
ca ca.crt
cert client.crt
key client.key
cipher AES-256-CBC
comp-lzo



然后就可以连接测试一下，如失败看一下客户端的日志，有的放矢。



## 三、通过用户名密码登录



证书登录有一个比较大的缺点，可以将证书拷贝给别的电脑此电脑就可以直接登录了，安全性较低，所以增加用户名密码登录方式。



### 1、增加用户名密码检查脚本



checkpsw.sh



```
###########################################################
# checkpsw.sh (C) 2004 Mathias Sundman 
#
# This script will authenticate OpenVPN users against
# a plain text file. The passfile should simply contain
# one row per user with the username first followed by
# one or more space(s) or tab(s) and then the password.
 
PASSFILE="/etc/openvpn/psw-file"
LOG_FILE="/etc/openvpn/openvpn-password.log"
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
```



### 2、配置 server.conf



在配置的最后增加以下内容：



```
script-security 3
auth-user-pass-verify /etc/openvpn/checkpsw.sh via-env
username-as-common-name
verify-client-cert none
```



### 3、创建 psw-file 文件，用于存放用户名和密码



```
[root@Wdp-host openvpn]# cat psw-file 
wdp 123456
test test
```



### 4、配置客户端 open 文件



注释掉密钥
;cert client.crt
;key client.key
在文件最后添加
auth-user-pass



### 5、重连测试，此时需要输入用户名及密码



## 四、固定客户端的 ip 地址



### 1、server.conf 中启动 ccd



client-config-dir ccd



在 ccd 文件夹下按照用户名创建文件



```
[root@Wdp-host openvpn]# ls
ccd          client    ipp.txt    openvpn-password.log  server       server.conf.bak
checkpsw.sh  easy-rsa  nohup.out  psw-file              server.conf
[root@Wdp-host openvpn]# cd ccd
[root@Wdp-host ccd]# ls
test  wdp
[root@Wdp-host ccd]# cat wdp
ifconfig-push 172.19.51.6 172.19.51.7
```



这地方经过测试有点问题，在此说明一下：
当客户端使用 3.3 版本时候 ipconfig-push x.x.x.x x.x.x.x+1 都可以，不用考虑 x 的值，但是如果使用的 2.4 左右的版本则需要配置 252 的掩码，也就是只能使用如下地址：https://editor.csdn.net/md/?articleId=119324734



### 2、重启服务器 openvpn 是进行测试



## 五、将 VPN 服务器端的内网地址推个客户端，添加到客户端的路由表中



配置 server.conf



```
push “route 1.70.0.0 255.255.0.0”
```



## 六、资源访问权限限制



通过 iptables 实现：



```
iptables -A FORWARD -s 172.16.103.13 -d 1.70.54.148 -j DROP
```



**配置 FORWARD 链中，禁止源地址 172.16.103.13 访问 1.70.54.148**