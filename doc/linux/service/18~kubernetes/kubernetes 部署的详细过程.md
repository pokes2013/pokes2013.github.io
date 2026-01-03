# kubeadm部署v1.18.5版本的详细过程

> 参考资料：
>
> 1.18.5
>
> https://www.cnblogs.com/lizhewei/p/13366172.html  
>
> 1.18.6
>
> https://www.cnblogs.com/smlile-you-me/p/13489642.html
>



## 一、部署前的准备

准备3台主机

|   名称   |    主机操作系统     |     硬件配置     |   ip地址    |
| :------: | :-----------------: | :--------------: | :---------: |
| master01 | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.40 |
|  work01  | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.44 |
|  work02  | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.45 |

```shell
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
```

### 1、关闭防火墙、selinux

各节点都需要执行

```shell
systemctl disable firewalld
systemctl stop firewalld
sed -i 's/^ *SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
reboot
```

### 2、关闭swap分区

各节点都需要执行

```
swapoff -a
sed -i 's/.*swap.*/#&/' /etc/fstab
```

或者

```shell
vim /etc/fstab
把这一行注释掉：
#/dev/mapper/centos-swap swap                    swap    defaults        0 0
保存退出重启三台机器
```

==关闭后必须重启三台机器==

### 3、配置主机名和IP(省略)

### 4、修改hosts文件

```
cat >> /etc/hosts << EOF    
10.10.30.40  master01
10.10.30.41  master02
10.10.30.44  work01
10.10.30.45  work02
EOF
```
### 5、各个节点免密登录
```
#生成ssh密钥，直接一路回车
ssh-keygen -t rsa
#复制刚刚生成的密钥到各节点可信列表中，需分别输入各主机密码
ssh-copy-id root@master01
ssh-copy-id root@work01
ssh-copy-id root@work02
```

### 6、主机间时间同步

各节点都需要执行

```shell
yum -y install ntpdate

crontab -e   #添加下面一行
0 */1 * * * ntpdate time.aliyun.com          #1小时同步1次
ntpdate time1.aliyun.com    #立即同步
```

### 7、启用内核模块

各个节点都需执行

```shell
cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#！/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
```
## 二、安装docker

各个节点都需执行

### 1、添加docker yum源

```
wget -O /etc/yum.repos.d/docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
yum makecache fast   #重建缓存
```

### 2、安装docker-ce

docker版本我们选择19.03.12，注意版本号不包含`:`与之前的数字

```
yum list docker-ce.x86_64 --showduplicates | sort -r
yum -y install docker-ce-19.03.12-3.el7
systemctl enable docker && systemctl start docker && docker version
```

### 3、确保网络模块开机自动加载

```
lsmod | grep overlay
lsmod | grep br_netfilter
```

若上面命令无返回值输出或提示文件不存在，需执行以下命令：

```
cat > /etc/modules-load.d/docker.conf <<EOF
overlay
br_netfilter
EOF

modprobe overlay
modprobe br_netfilter
```

### 4、添加网桥过滤及地址转发

各节点均需执行，使桥接流量对iptables可见

方法一：

```
cat > /etc/sysctl.d/k8s.conf <<EOF
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
EOF
sysctl --system
```

验证是否生效，均返回 1 即正确

```
sysctl -n net.bridge.bridge-nf-call-iptables
sysctl -n net.bridge.bridge-nf-call-ip6tables
```

方法二：

```shell
vim /etc/sysctl.conf    #末尾添加以下内容
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
vm.swappiness = 0
```
```shell
sysctl -p    #刷新配置
```
==提示没有这个文件，忽略它因为我们后续才会生成这个文件。==

### 5、修改docker配置文件

修改之前查看一下cgroup的驱动，我们知道docker是利用linux的cgroup来管理容器。

```
docker info | grep -i cgroup
```

可以看到cgroup驱动是：`cgroupfs` ，但是k8s默认使用的驱动是systemd，所以我们必须修改其配置让它和K8s一致。

```
#修改cgroup驱动为systemd[k8s官方推荐]、限制容器日志量、修改存储类型，最后的docker家目录可修改

$ cat > /etc/docker/daemon.json <<EOF
{
  "exec-opts": ["native.cgroupdriver=systemd"],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "100m"
  },
  "storage-driver": "overlay2",
  "storage-opts": [
    "overlay2.override_kernel_check=true"
  ],
  "registry-mirrors": ["https://7uuu3esz.mirror.aliyuncs.com"],
  "data-root": "/data/docker"
}
EOF


#添加开机自启，立即启动
$ systemctl enable --now docker
```



修改的方法有两种，vim打开下面的文件：

```
vim /usr/lib/systemd/system/docker.service
```

方法一：找到下面这一项`ExecStart=/usr/bin/dockerd`    修改-H后面的参数

方法二：修改docker守护进程的文件

```
vim /usr/lib/systemd/system/docker.service
找到下面这一项
ExecStart=/usr/bin/dockerd    #如果源文件此行后面有-H选项，请删除-H及后面所有内容


cat > /etc/docker/daemon.json << EOF
{
      "exec-opts": ["native.cgroupdriver=systemd"]
      "registry-mirrors": ["https://tue4pc99.mirror.aliyuncs.com"]
}
EOF

systemctl restart docker
systemctl status docker

还可以这样写：systemctl enable --now docker  #开机自启，立即启动

docker info | grep -i cgroup
```

当你看到cgroup驱动为systemd，就证明你配置成功了



## 三、部署kubernetes集群

### 添加kubernetes源

各个节点都需执行

```shell
cat > /etc/yum.repos.d/kubernetes.repo << EOF
 
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=0
repo_gpgcheck=0
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

### 安装三个kube软件

master节点执行安装kubeadm、kubelet、kubectl共三个

work节点安装kubeadm、kubelet这两个，而kubectl不需要在work节点安装。即使安装也无法使用。

我们这里选择1.18.5的版本进行安装

```
yum list kubeadm.x86_64 --showduplicates | sort -r    #查看版本并排序
```

```
yum -y install --setopt=obsoletes=0 kubeadm-1.18.5-0 kubelet-1.18.5-0 kubectl-1.18.5-0

systemctl start kubelet
systemctl enable kubelet
systemctl status kubelet
```

我们看到启动失败，错误码rror(255)。因为没有配置文件，它的配置文件将由kubeadm在初始化的过程中生成。

### 配置自动补全命令

```
#安装bash自动补全插件
yum install bash-completion -y
#设置kubectl与kubeadm命令补全，下次login生效
kubectl completion bash >/etc/bash_completion.d/kubectl
kubeadm completion bash > /etc/bash_completion.d/kubeadm
```



### 预拉取kubernetes镜像

拉去之前我们必须先查看确认我们需要的镜像是什么。

```
kubeadm config images list --kubernetes-version v1.18.5
```

查看指定k8s版本需要哪些镜像

```shell
[root@master01 ~]# kubeadm config images list --kubernetes-version v1.18.5
W1002 16:30:16.683325    1492 configset.go:202] WARNING: kubeadm cannot validate component configs for API groups [kubelet.config.k8s.io kubeproxy.config.k8s.io]
k8s.gcr.io/kube-apiserver:v1.18.5
k8s.gcr.io/kube-controller-manager:v1.18.5
k8s.gcr.io/kube-scheduler:v1.18.5
k8s.gcr.io/kube-proxy:v1.18.5
k8s.gcr.io/pause:3.2
k8s.gcr.io/etcd:3.4.3-0
k8s.gcr.io/coredns:1.6.7
```

通过国内源进行拉去，具体操作请查阅博客：

https://blog.csdn.net/annita2019/article/details/108903414



### 集群初始化

```shell
kubeadm init --kubernetes-version=v1.18.5 \
--image-repository registry.aliyuncs.com/google_containers \
--pod-network-cidr=10.244.0.0/16 \
--apiserver-advertise-address 10.10.30.40
```

- 初始化master 10.244.0.0/16是flannel固定使用的IP段，设置取决于网络组件要求；
- 10.10.30.40是我的master节点IP

一次性成功

```shell
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.10.30.40:6443 --token efdqq9.f7vtj4hizippumir \
    --discovery-token-ca-cert-hash sha256:7707ee289438f390c8002982b16afe082c5c5a91c4024de82fcdf8efe8592d12
```

如果没有一次性成功，需要第二次时必须要reset一下，防止第二次受到第一次的影响。

```
kubeadm reset
```

先看一下集群中有哪些节点

```SHELL
[root@master01 ~]# kubectl get node
NAME       STATUS     ROLES    AGE     VERSION
master01   NotReady   master   8m54s   v1.18.5

[root@master01 ~]# kubectl get cs
NAME                 STATUS    MESSAGE             ERROR
scheduler            Healthy   ok                  
controller-manager   Healthy   ok                  
etcd-0               Healthy   {"health":"true"} 
```

### 安装网络组件（flannel）

```
mkdir -p /root/k8s
cd /root/k8s
wget https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
kubectl apply -f kube-flannel.yml

[root@master01 ~]# kubectl apply -f kube-flannel.yml
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds created
[root@master01 ~]# kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
master01   Ready    master   19m   v1.18.5
```

如果STATUS提示NotReady，可以通过 kubectl describe node kube-master 查看具体的描述信息，性能差的服务器到达Ready状态时间会长些

### work节点加入集群

work01和work02节点执行

```
kubeadm join 10.10.30.40:6443 --token efdqq9.f7vtj4hizippumir \
    --discovery-token-ca-cert-hash sha256:7707ee289438f390c8002982b16afe082c5c5a91c4024de82fcdf8efe8592d12
```

然后在master节点查看，如果机器性能差，可能会等的时间较长。

```
[root@master01 ~]# kubectl get nodes
NAME       STATUS   ROLES    AGE   VERSION
master01   Ready    master   23m   v1.18.5
work01     Ready    <none>   61s   v1.18.5
work02     Ready    <none>   66s   v1.18.5
```

