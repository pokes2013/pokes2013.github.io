###################################################################
# File Name: openvpn.sh
# Author: xunyin
# E-mail: lnhxzwb@126.com
# Created Time: Thu 21 Nov 2019 03:38:48 PM CST
#==================================================================
#!/bin/bash

#canshu_num=$#
xuan_ze=$1
vpn_user=$2

#docker是否安装查检
docker_check()
{
docker_rpm=$(rpm -qa |grep docker |wc -l)
if [ ${docker_rpm} -gt 0 ];then
echo "docker is already installed"
docker_conf
else
yum install yum-utils device-mapper-persistent-data lvm2 -y
wget -O /etc/yum.repos.d/docker-ce.repo https://download.docker.com/linux/centos/docker-ce.repo
sed -i 's+download.docker.com+mirrors.tuna.tsinghua.edu.cn/docker-ce+' /etc/yum.repos.d/docker-ce.repo
yum makecache fast -y
yum install docker -y
docker_conf
fi
}

#docker配置
docker_conf()
{
cat >/etc/docker/daemon.json <<EOF
{
"registry-mirrors": ["https://lgc971x1.mirror.aliyuncs.com"]
}
EOF
systemctl start docker
systemctl enable docker
docker pull kylemanna/openvpn:2.4
mkdir -p /data/openvpn/conf
}


vpn_config()
{
#生成配置文件
read -p "请输入公网IP: " ip
docker run -v /data/openvpn:/etc/openvpn --rm kylemanna/openvpn:2.4 ovpn_genconfig -u udp://${ip}
#生成密钥文件
cat <<EOF
===========================================<信息提示>======================================
输入私钥密码（输入时是看不见的,12345678为例，请根据实际情况输入）：
Enter PEM pass phrase:12345678
再输入一遍
Verifying - Enter PEM pass phrase:12345678
输入一个CA名称（我这里直接回车）
Common Name (eg: your user, host, or server name) [Easy-RSA CA]:
输入刚才设置的私钥密码（输入完成后会再让输入一次）
Enter pass phrase for /etc/openvpn/pki/private/ca.key:12345678
==============================================================================================
EOF
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 ovpn_initpki
#启动openvpn
docker run --name openvpn -v /data/openvpn:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn:2.4
}

# 安装VPN
install_vpn()
{
docker_check
vpn_config
name=$(docker ps |awk '/openvpn/ {print $NF}')
if [ "$name" = "openvpn" ];then
touch /data/openvpn/openvpn.lock
cp -rf ./openvpn.sh /usr/local/bin/openvpn
cat <<EOF
================================================<成功提示>===============================================
Openvpn 已安装成功，请创建用户后使用
========================================================================================================
EOF
else
cat <<EOF
================================================<错误提示>================================================
Openvpn 安装失败，请检查后操作!
EOF
exit 1
fi
}

#删除VPN用户
vpn_del_user()
{
# read -p "请输入删除的用户名: " vpn_user
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 easyrsa revoke ${vpn_user}
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 easyrsa gen-crl
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 rm -f /etc/openvpn/pki/reqs/"${vpn_user}".req
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 rm -f /etc/openvpn/pki/private/"${vpn_user}".key
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 rm -f /etc/openvpn/pki/issued/"${vpn_user}".crt
docker restart openvpn
echo "================================================<成功提示>================================================"
echo " 注销并已删除vpn用户:${vpn_user}成功!"
echo "=========================================================================================================="
}

#添加VPN用户
vpn_add_user()
{
# read -p "请输入添加新的用户名: " vpn_user
if [ -e "/data/openvpn/conf/${vpn_user}.ovpn" ];then
echo "================================================<温馨提示>================================================"
echo "VPN用户：${vpn_user}已存在,请检查后操作!!"
echo "========================================================================================================="
else
docker run -v /data/openvpn:/etc/openvpn --rm -it kylemanna/openvpn:2.4 easyrsa build-client-full ${vpn_user} nopass
docker run -v /data/openvpn:/etc/openvpn --rm kylemanna/openvpn:2.4 ovpn_getclient ${vpn_user} > /data/openvpn/conf/${vpn_user}.ovpn
docker restart openvpn
cat <<EOF
================================================<成功提示>=================================================
新建vpn用户:${vpn_user}成功!"
=========================================================================================================
新建vpn用户:${vpn_user} 密钥已生成在/data/openvpn/conf/${vpn_user}.ovpn ，请自行获取！！！"
==========================================================================================================
EOF
fi
}


help()
#帮助函数
{
cat <<EOF
================================================<帮助提示>================================================
添加vpn用户执行命令: openvpn add vpn用户名
删除vpn用户执行命令: openvpn del vpn用户名
安装VPN执行命令:openvpn.sh install
=========================================================================================================
EOF
}


main()
{

if [ "${xuan_ze}" = "add" ];then
vpn_add_user
elif [ "${xuan_ze}" = "install" ];then
if [ ! -e /data/openvpn/openvpn.lock ];then
install_vpn
else
echo "================================================<信息提示>================================================"
echo "Openvpn已经安装，请检查后操作!"
exit 1
fi
elif [ "${xuan_ze}" = "del" ];then
vpn_del_user
else
echo "================================================<错误提示>================================================"
echo " 输入参数类型无效,类型只包含add|install|del"
help
fi
}

main
