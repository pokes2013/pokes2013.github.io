# k8s的部署

参考资料：

镜像下载   https://blog.csdn.net/networken/article/details/84571373







## 一、准备主机操作系统及环境

|   名称   |    主机操作系统     |     硬件配置     |   ip地址    |
| :------: | :-----------------: | :--------------: | :---------: |
| master01 | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.40 |
|  work01  | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.44 |
|  work02  | CentOS7.7最小化安装 | 2CPU/内存2G/100G | 10.10.30.45 |

安装系统过程中是==自动分区==，这就意味着我们必须手动关闭Swap分区。

```
[root@localhost ~]# cat /etc/redhat-release
CentOS Linux release 7.7.1908 (Core)
```

### 1、更改主机名

### 2、更改IP地址

### 3、关闭防火墙和SElinux

```
systemctl disable firewalld
systemctl stop firewalld
sed -i 's/^ *SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
reboot
```

==必须重启==

### 4、主机时间同步

方法一：在master节点搭建ntp服务（待写）

方法二：使用阿里云的时钟源

```
yum -y install ntpdate

crontab -e
添加下面一行
0 */1 * * * ntpdate time.aliyun.com          #1小时同步1次
保存退出
ntpdate time1.aliyun.com    #立即同步
```

### 5、关闭Swap分区

```
vim /etc/fstab

把这一行注释掉：
#/dev/mapper/centos-swap swap                    swap    defaults        0 0
保存退出重启三台机器
```

验证Swap分区

```
[root@work02 ~]# free -m  #重启前Swap状态
              total        used        free      shared  buff/cache   available
Mem:           1846         121        1490           9         234        1578
Swap:          3839           0        3839

[root@work02 ~]# reboot

[root@master01 ~]# free -m  #重启后Swap状态
              total        used        free      shared  buff/cache   available
Mem:           1846         113        1633           9          99        1605
Swap:             0           0           0
```



### 6、配置主机网桥过滤

添加网桥过滤及地址转发

```
vim /etc/sysctl.d/k8s.conf
创建K8S.conf文件，添加以下内容

net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
vm.swappiness = 0
```

加载br_netfilter模块

```
[root@work01 ~]# modprobe br_netfilter
[root@work01 ~]# lsmod | grep br_netfilter    #查看是否加载成功
br_netfilter           22256  0 
bridge                151336  1 br_netfilter
```

加载网桥过滤配置文件

```
[root@work01 ~]# sysctl -p /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-ip6tables = 1
net.bridge.bridge-nf-call-iptables = 1
net.ipv4.ip_forward = 1
vm.swappiness = 0
```

### 7、开启ipvs

由于k8s在使用service的过程中，需要用到ipvstable。因为ipvs转换效率比ipvstable要高，所以我们这里选择ipvs。

#### 安装ipset和ipvsadm

```
yum -y install ipset ipvsadm
```

#### 添加需要加载的模块

```
vim /etc/sysconfig/modules/ipvs.modules

添加以下内容
#！/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
保存退出
```

或者直接这样

```
cat > /etc/sysconfig/modules/ipvs.modules <<EOF
#！/bin/bash
modprobe -- ip_vs
modprobe -- ip_vs_rr
modprobe -- ip_vs_wrr
modprobe -- ip_vs_sh
modprobe -- nf_conntrack_ipv4
EOF
```

授权、运行、检查是否加载

```
chmod 755 /etc/sysconfig/modules/ipvs.modules
bash /etc/sysconfig/modules/ipvs.modules
lsmod | grep -e ip_vs -e nf_conntrack
```

```
[root@work01 ~]# lsmod | grep -e ip_vs -e nf_conntrack
nf_conntrack_ipv4      15053  0 
nf_defrag_ipv4         12729  1 nf_conntrack_ipv4
ip_vs_sh               12688  0 
ip_vs_wrr              12697  0 
ip_vs_rr               12600  0 
ip_vs                 145497  6 ip_vs_rr,ip_vs_sh,ip_vs_wrr
nf_conntrack          139224  2 ip_vs,nf_conntrack_ipv4
libcrc32c              12644  3 xfs,ip_vs,nf_conntrack
```

### 8、安装docker-ce

在master和work节点安装指定版本的docker-ce，为什么要安装docker-ce呢？k8s集群不能直接管理集群吗？答案是不能，K8S管理的最小单位是Pod，Pod中可以包含相应的容器，因此k8s需要借助docker-ce这种容器管理工具。

为什么要安装指定版本的docker-ce？因为有一些docker-ce 安装完成之后需要更改很多的内容，比如：服务启动文件、iptables默认规则链策略等。那么在这里我们不想给大家造成那么多的麻烦，因此我们需要安装指定版本的docker-ce

#### 更换docker的yum源下载地址

```
wget -O /etc/yum.repos.d/docker-ce.repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

```
[root@work02 ~]# ll /etc/yum.repos.d/
总用量 48
-rw-r--r--. 1 root root 2523 6月  16 2018 CentOS-Base.repo
-rw-r--r--. 1 root root 1664 9月   5 2019 CentOS-Base.repo.bak
-rw-r--r--. 1 root root 1309 9月   5 2019 CentOS-CR.repo
-rw-r--r--. 1 root root  649 9月   5 2019 CentOS-Debuginfo.repo
-rw-r--r--. 1 root root  314 9月   5 2019 CentOS-fasttrack.repo
-rw-r--r--. 1 root root  630 9月   5 2019 CentOS-Media.repo
-rw-r--r--. 1 root root 1331 9月   5 2019 CentOS-Sources.repo
-rw-r--r--. 1 root root 6639 9月   5 2019 CentOS-Vault.repo
-rw-r--r--  1 root root 2640 3月  16 2020 docker-ce.repo
-rw-r--r--. 1 root root  664 5月  11 2018 epel.repo
-rw-r--r--. 1 root root 1149 9月  18 2019 epel-testing.repo
```



#### 查看docker-ce版本

对版本进行排序

```
yum list docker-ce.x86_64 --showduplicates | sort -r
```

安装指定版本的docker-ce

```
yum -y install --setopt=obsoletes=0 docker-ce-18.06.3.ce-3.el7
```

```
[root@work02 ~]# docker version
Client:
 Version:           18.06.3-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        d7080c1
 Built:             Wed Feb 20 02:26:51 2019
 OS/Arch:           linux/amd64
 Experimental:      false
Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

==三个主机必须安装同样的版本==

Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?   

提示我们没有启动，因此三台节点都要启动docker-ce

```
[root@work02 ~]# systemctl enable docker
Created symlink from /etc/systemd/system/multi-user.target.wants/docker.service to /usr/lib/systemd/system/docker.service.
[root@work02 ~]# systemctl start docker
[root@work02 ~]# docker version
Client:
 Version:           18.06.3-ce
 API version:       1.38
 Go version:        go1.10.3
 Git commit:        d7080c1
 Built:             Wed Feb 20 02:26:51 2019
 OS/Arch:           linux/amd64
 Experimental:      false

Server:
 Engine:
  Version:          18.06.3-ce
  API version:      1.38 (minimum version 1.12)
  Go version:       go1.10.3
  Git commit:       d7080c1
  Built:            Wed Feb 20 02:28:17 2019
  OS/Arch:          linux/amd64
  Experimental:     false

```

现在我们可以看见server了,没有启动之前是没有server的。但是现在还有一个问题，如果docker-ce未来想使用第三方的一些配置，那么我们还需要添加相应的配置文件。

#### 修改docker-ce服务配置文件

如果你安装的是其他版本的docker-ce，需要对配置文件进行修改：

```
vim /usr/lib/systemd/system/docker.service
找到下面这一项
ExecStart=/usr/bin/dockerd    #如果源文件此行后面有-H选项，请删除-H及后面所有内容
```

而我们使用的18.06.3-ce版本是没有的，所以不需要修改。==注意：有些版本不需要修改，请注意观察==

```
[Unit]
Description=Docker Application Container Engine
Documentation=https://docs.docker.com
After=network-online.target firewalld.service
Wants=network-online.target

[Service]
Type=notify
# the default is not to use systemd for cgroups because the delegate issues still
# exists and systemd currently does not support the cgroup feature set required
# for containers run by docker
ExecStart=/usr/bin/dockerd
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process
# restart the docker process if it exits prematurely
Restart=on-failure
StartLimitBurst=3
StartLimitInterval=60s

[Install]
WantedBy=multi-user.target
```

接下来，还需要创建`/etc/docker/daemon.json`文件，使docker按照我们的意愿去完成相应的工作。比如：docker所使用的cgroup的驱动，假如未来我们需要用docker部署gitlab这种私有仓库，我们也可以在这里添加。本次我们在这个地方给docker添加一个原生的cgroup的驱动来对我们的docker容器进行一个限制。

```
vim /etc/docker/daemon.json
添加下面内容

{
      "exec-opts": ["native.cgroupdriver=systemd"]
}

完成后重启docker

[root@work02 ~]# systemctl restart docker
[root@work02 ~]# systemctl status docker
● docker.service - Docker Application Container Engine
   Loaded: loaded (/usr/lib/systemd/system/docker.service; enabled; vendor preset: disabled)
   Active: active (running) since 四 2020-10-01 00:45:46 CST; 1min 7s ago
     Docs: https://docs.docker.com
 Main PID: 14731 (dockerd)
    Tasks: 21
   Memory: 44.9M
   CGroup: /system.slice/docker.service
           ├─14731 /usr/bin/dockerd
           └─14738 docker-containerd --config /var/run/docker/containerd/c...

10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.160444...c
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.160534...c
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.160546..."
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.433079..."
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.543585..."
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.665248...e
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.665442..."
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.666721..."
10月 01 00:45:46 work02 systemd[1]: Started Docker Application Container....
10月 01 00:45:46 work02 dockerd[14731]: time="2020-10-01T00:45:46.750997..."
Hint: Some lines were ellipsized, use -l to show in full.
```

## 二、Kubernetes集群软件安装

### 1、软件信息

所有k8s集群节点均需安装，默认yum源是谷歌，可以使用阿里云yum源

| 需求 |       kubeadm        |                    kubelet                    |      kubectl       | docker-ce |
| :--: | :------------------: | :-------------------------------------------: | :----------------: | :-------: |
| 功能 | 初始化集群，管理集群 | 用于接受api-server指令，对pod生命周期进行管理 | 集群命令行管理工具 |     /     |
| 版本 |        1.17.2        |                    1.17.2                     |       1.17.2       |  18.06.3  |

### 2、更换yum源

```
cat > /etc/yum.repos.d/kubernetes.repo << EOF
 
[kubernetes]
name=Kubernetes
baseurl=https://mirrors.aliyun.com/kubernetes/yum/repos/kubernetes-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
       https://mirrors.aliyun.com/kubernetes/yum/doc/rpm-package-key.gpg
EOF
```

验证一下添加的yum源是否可用

```
[root@work02 ~]# yum list | grep kubeadm
导入 GPG key 0xA7317B0F:      #说是要导入一个key,输入一个y
 用户ID     : "Google Cloud Packages Automatic Signing Key <gc-team@google.com>"
 指纹       : d0bc 747f d8ca f711 7500 d6fa 3746 c208 a731 7b0f
 来自       : https://mirrors.aliyun.com/kubernetes/yum/doc/yum-key.gpg
 y
 kubeadm.x86_64                            1.19.2-0                     kubernetes
```

### 3、安装指定版本软件

kubeadm、kubelet、kubectl

```
yum -y install --setopt=obsoletes=0 kubeadm-1.17.2-0 kubelet-1.17.2-0 kubectl-1.17.2-0
```

### 4、配置kubelet

kubeadm、kubectl暂时用不到，我们先配置kubelet，如果不配置可能会导致k8s集群无法启动。

为了实现docker使用cgroupdriver与kubelet使用的cgroup的一致性，建议修改如下文件内容：

```
vim /etc/sysconfig/kubelet
修改：
KUBELET_EXTRA_ARGS="--cgroup-driver=systemd"
保存退出

[root@master01 ~]# systemctl enable kubelet
```

在这里需要注意的是，只要设置开机启动就可以了，==千万不要启动==。因为它现在还没有配置文件，它的配置文件将由kubeadm在初始化的过程中生成。

```
[root@master01 ~]# systemctl status kubelet
● kubelet.service - kubelet: The Kubernetes Node Agent
   Loaded: loaded (/usr/lib/systemd/system/kubelet.service; enabled; vendor preset: disabled)
  Drop-In: /usr/lib/systemd/system/kubelet.service.d
           └─10-kubeadm.conf
   Active: inactive (dead)
     Docs: https://kubernetes.io/docs/
```

我们看见kubelet已经成功设置开机自启动。

## 三、Kubernetes集群镜像准备

### 1、查询需要的镜像

==三台机器都需要下载==，如果你的网速不好，那么可以在1台中下载好，打包传到其他2台机器

查看集群使用的容器镜像

```
[root@master01 ~]# kubeadm config images list
I1001 04:42:25.062236   19895 version.go:251] remote version is much newer: v1.19.2; falling back to: stable-1.17
W1001 04:42:26.153555   19895 validation.go:28] Cannot validate kube-proxy config - no validator is available
W1001 04:42:26.153595   19895 validation.go:28] Cannot validate kubelet config - no validator is available
k8s.gcr.io/kube-apiserver:v1.17.12
k8s.gcr.io/kube-controller-manager:v1.17.12
k8s.gcr.io/kube-scheduler:v1.17.12
k8s.gcr.io/kube-proxy:v1.17.12
k8s.gcr.io/pause:3.1
k8s.gcr.io/etcd:3.4.3-0
k8s.gcr.io/coredns:1.6.5
```

==出现大坑，这里坑了我2个小时==，非常严重的坑。上面显示我需要的镜像是：

```
k8s.gcr.io/kube-apiserver:v1.17.12
k8s.gcr.io/kube-controller-manager:v1.17.12
k8s.gcr.io/kube-scheduler:v1.17.12
k8s.gcr.io/kube-proxy:v1.17.12
```

我提前下载好之后，kubeadm init时显示我没有镜像。于是我删除提前下载好的所有镜像kubeadm init 让它自动下载所需镜像，结果它下载的不是v1.17.12而是v1.17.2，说明上面查出来所需的版本是错的。这里大家注意一下。

### 2、下载所需镜像

```
docker pull registry.aliyuncs.com/google_containers/kube-apiserver:v1.17.2 && \
docker pull registry.aliyuncs.com/google_containers/kube-controller-manager:v1.17.2&& \
docker pull registry.aliyuncs.com/google_containers/kube-scheduler:v1.17.2 && \
docker pull registry.aliyuncs.com/google_containers/kube-proxy:v1.17.2 && \
docker pull registry.aliyuncs.com/google_containers/pause:3.1 && \
docker pull registry.aliyuncs.com/google_containers/etcd:3.4.3-0 && \
docker pull registry.aliyuncs.com/google_containers/coredns:1.6.5
```



### 3、集群初始化

==只在master操作==

```
kubeadm init --kubernetes-version=v1.17.2 \
--image-repository registry.aliyuncs.com/google_containers \
--pod-network-cidr=172.16.0.0/16 \
--apiserver-advertise-address 10.10.30.40
```

有点慢，等待几分钟就好了

- 172.16.0.0/16是pod网络
- 10.10.30.40 是master主机IP



显示以下结果证明成功

```
Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.10.30.40:6443 --token ur5qbt.qcgm5dsnmzcak5av \
    --discovery-token-ca-cert-hash sha256:f1f55b77f926e7698a47d2d16c7610d05e25cfc2baa775b448c6ed9fae003854
```

记录启动过程到记事本，后续需要用。

```
[root@master01 ~]# kubeadm init --kubernetes-version=v1.17.2 \
> --image-repository registry.aliyuncs.com/google_containers \
> --pod-network-cidr=172.16.0.0/16 \
> --apiserver-advertise-address 10.10.30.40

启动过程：

W1001 12:20:16.596808    1957 validation.go:28] Cannot validate kube-proxy config - no validator is available
W1001 12:20:16.596848    1957 validation.go:28] Cannot validate kubelet config - no validator is available
[init] Using Kubernetes version: v1.17.2
[preflight] Running pre-flight checks
	[WARNING Hostname]: hostname "master01" could not be reached
	[WARNING Hostname]: hostname "master01": lookup master01 on 114.114.114.114:53: no such host
[preflight] Pulling images required for setting up a Kubernetes cluster
[preflight] This might take a minute or two, depending on the speed of your internet connection
[preflight] You can also perform this action in beforehand using 'kubeadm config images pull'
[kubelet-start] Writing kubelet environment file with flags to file "/var/lib/kubelet/kubeadm-flags.env"
[kubelet-start] Writing kubelet configuration to file "/var/lib/kubelet/config.yaml"
[kubelet-start] Starting the kubelet
[certs] Using certificateDir folder "/etc/kubernetes/pki"
[certs] Generating "ca" certificate and key
[certs] Generating "apiserver" certificate and key
[certs] apiserver serving cert is signed for DNS names [master01 kubernetes kubernetes.default kubernetes.default.svc kubernetes.default.svc.cluster.local] and IPs [10.96.0.1 10.10.30.40]
[certs] Generating "apiserver-kubelet-client" certificate and key
[certs] Generating "front-proxy-ca" certificate and key
[certs] Generating "front-proxy-client" certificate and key
[certs] Generating "etcd/ca" certificate and key
[certs] Generating "etcd/server" certificate and key
[certs] etcd/server serving cert is signed for DNS names [master01 localhost] and IPs [10.10.30.40 127.0.0.1 ::1]
[certs] Generating "etcd/peer" certificate and key
[certs] etcd/peer serving cert is signed for DNS names [master01 localhost] and IPs [10.10.30.40 127.0.0.1 ::1]
[certs] Generating "etcd/healthcheck-client" certificate and key
[certs] Generating "apiserver-etcd-client" certificate and key
[certs] Generating "sa" key and public key
[kubeconfig] Using kubeconfig folder "/etc/kubernetes"
[kubeconfig] Writing "admin.conf" kubeconfig file
[kubeconfig] Writing "kubelet.conf" kubeconfig file
[kubeconfig] Writing "controller-manager.conf" kubeconfig file
[kubeconfig] Writing "scheduler.conf" kubeconfig file
[control-plane] Using manifest folder "/etc/kubernetes/manifests"
[control-plane] Creating static Pod manifest for "kube-apiserver"
[control-plane] Creating static Pod manifest for "kube-controller-manager"
W1001 12:20:20.295198    1957 manifests.go:214] the default kube-apiserver authorization-mode is "Node,RBAC"; using "Node,RBAC"
[control-plane] Creating static Pod manifest for "kube-scheduler"
W1001 12:20:20.296260    1957 manifests.go:214] the default kube-apiserver authorization-mode is "Node,RBAC"; using "Node,RBAC"
[etcd] Creating static Pod manifest for local etcd in "/etc/kubernetes/manifests"
[wait-control-plane] Waiting for the kubelet to boot up the control plane as static Pods from directory "/etc/kubernetes/manifests". This can take up to 4m0s
[apiclient] All control plane components are healthy after 35.505943 seconds
[upload-config] Storing the configuration used in ConfigMap "kubeadm-config" in the "kube-system" Namespace
[kubelet] Creating a ConfigMap "kubelet-config-1.17" in namespace kube-system with the configuration for the kubelets in the cluster
[upload-certs] Skipping phase. Please see --upload-certs
[mark-control-plane] Marking the node master01 as control-plane by adding the label "node-role.kubernetes.io/master=''"
[mark-control-plane] Marking the node master01 as control-plane by adding the taints [node-role.kubernetes.io/master:NoSchedule]
[bootstrap-token] Using token: 9zv18c.jfukelpmhv22an4n
[bootstrap-token] Configuring bootstrap tokens, cluster-info ConfigMap, RBAC Roles
[bootstrap-token] configured RBAC rules to allow Node Bootstrap tokens to post CSRs in order for nodes to get long term certificate credentials
[bootstrap-token] configured RBAC rules to allow the csrapprover controller automatically approve CSRs from a Node Bootstrap Token
[bootstrap-token] configured RBAC rules to allow certificate rotation for all node client certificates in the cluster
[bootstrap-token] Creating the "cluster-info" ConfigMap in the "kube-public" namespace
[kubelet-finalize] Updating "/etc/kubernetes/kubelet.conf" to point to a rotatable kubelet client certificate and key
[addons] Applied essential addon: CoreDNS
[addons] Applied essential addon: kube-proxy

Your Kubernetes control-plane has initialized successfully!

To start using your cluster, you need to run the following as a regular user:

  mkdir -p $HOME/.kube
  sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
  sudo chown $(id -u):$(id -g) $HOME/.kube/config

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 10.10.30.40:6443 --token 9zv18c.jfukelpmhv22an4n \
    --discovery-token-ca-cert-hash sha256:3e65eb3f27ee00ecc91e9c5f747b8ea39cb09d9781e79e1c00da91d3dcf36508 

```

上面记录了完成的初始化输出的内容，根据输出的内容基本上可以看出手动初始化安装一个Kubernetes集群所需要的关键步骤。

> 其中有以下关键内容：
>
> - `[kubelet-start]` 生成kubelet的配置文件”`/var/lib/kubelet/config.yaml`”
>
> - `[certificates]`生成相关的各种证书
>
> - `[kubeconfig]`生成相关的`kubeconfig`文件
>
> - `[bootstraptoken]`生成token记录下来，后边使用kubeadm join往集群中添加节点时会用到
>
> - 下面的命令是配置常规用户如何使用kubectl访问集群：
>
> ```html
>     mkdir -p $HOME/.kube
>     sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
>     sudo chown $(id -u):$(id -g) $HOME/.kube/config
> ```
>
> - 要求我们部署集群网络
>
> ```
> You should now deploy a pod network to the cluster.  
> Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
>   https://kubernetes.io/docs/concepts/cluster-administration/addons/
>   
> 翻译：
> 现在应该将pod网络部署到集群。
> 使用下列选项之一运行“kubectl apply-f[podnetwork].yaml”：
> https://kubernetes.io/docs/concepts/cluster-administration/addons/
> ```
>
> - 最后给出了将节点加入集群的命令
>
>
>   ```
>   Then you can join any number of worker nodes by running the following on each as root:
>   然后，您可以通过以root身份在每个工作节点上运行以下命令来连接任意数量的工作节点：
>   
>   kubeadm join 10.10.30.40:6443 --token 9zv18c.jfukelpmhv22an4n \
>       --discovery-token-ca-cert-hash sha256:3e65eb3f27ee00ecc91e9c5f747b8ea39cb09d9781e79e1c00da91d3dcf36508
>   ```
>
>  查看一下节点
>
> ```
> [root@master01 ~]# kubectl get node
> NAME       STATUS     ROLES    AGE    VERSION
> master01   NotReady   master   157m   v1.17.2
> ```
>
> 节点是NotReady状态，因为我们还需要一个扁平化的网络。

> 这里我们先查看一下状态，确认各个组件都处于healthy状态。
>
> ```
> [root@master01 ~]# kubectl get cs
> NAME                 STATUS    MESSAGE             ERROR
> scheduler            Healthy   ok                  
> controller-manager   Healthy   ok                  
> etcd-0               Healthy   {"health":"true"} 
> ```
>
> 
>
> 
>
> 再查看后台运行的容器
>
> ```
> [root@master01 ~]# docker ps
> CONTAINER ID        IMAGE                                               COMMAND                  CREATED             STATUS              PORTS               NAMES
> ad62a8f2b408        cba2a99699bd                                        "/usr/local/bin/kube…"   3 minutes ago       Up 3 minutes                            k8s_kube-proxy_kube-proxy-6nqxx_kube-system_905fa1fa-cbd6-4456-8a92-5d0ea61a53b9_0
> 962ce4b7356f        registry.aliyuncs.com/google_containers/pause:3.1   "/pause"                 3 minutes ago       Up 3 minutes                            k8s_POD_kube-proxy-6nqxx_kube-system_905fa1fa-cbd6-4456-8a92-5d0ea61a53b9_0
> ae6a8c20939e        da5fd66c4068                                        "kube-controller-man…"   3 minutes ago       Up 3 minutes                            k8s_kube-controller-manager_kube-controller-manager-master01_kube-system_4bb849cdc3366bf40af382de90c674e2_0
> 7fd2792f9a23        303ce5db0e90                                        "etcd --advertise-cl…"   3 minutes ago       Up 3 minutes                            k8s_etcd_etcd-master01_kube-system_06f4192c0d33463004101daeccdaf3c1_0
> 612fa158a007        41ef50a5f06a                                        "kube-apiserver --ad…"   3 minutes ago       Up 3 minutes                            k8s_kube-apiserver_kube-apiserver-master01_kube-system_7b33948038ea3ef997949eceef3397d9_0
> 6693e8fb687b        f52d4c527ef2                                        "kube-scheduler --au…"   3 minutes ago       Up 3 minutes                            k8s_kube-scheduler_kube-scheduler-master01_kube-system_5fd6ddfbc568223e0845f80bd6fd6a1a_0
> 407a66de12c7        registry.aliyuncs.com/google_containers/pause:3.1   "/pause"                 3 minutes ago       Up 3 minutes                            k8s_POD_kube-controller-manager-master01_kube-system_4bb849cdc3366bf40af382de90c674e2_0
> f328ef4749c1        registry.aliyuncs.com/google_containers/pause:3.1   "/pause"                 3 minutes ago       Up 3 minutes                            k8s_POD_kube-scheduler-master01_kube-system_5fd6ddfbc568223e0845f80bd6fd6a1a_0
> b8c1b2f800a4        registry.aliyuncs.com/google_containers/pause:3.1   "/pause"                 3 minutes ago       Up 3 minutes                            k8s_POD_kube-apiserver-master01_kube-system_7b33948038ea3ef997949eceef3397d9_0
> 16034e3c8aaa        registry.aliyuncs.com/google_containers/pause:3.1   "/pause"                 3 minutes ago       Up 3 minutes                            k8s_POD_etcd-master01_kube-system_06f4192c0d33463004101daeccdaf3c1_0
> ```
>

接下来我们就按提示操作做就OK了

### 4、配置运行身份

创建.kube，复制admin.conf，更改所属

- 在家目录创建隐藏目录.kube
- 复制初始化过程中生成的admin.conf到.kube
- 更改所属用户、所属组（这一步我们不用改，我们用的是root，后续管理也用root）

```
[root@master01 ~]# cd ~
[root@master01 ~]# mkdir .kube
[root@master01 ~]# cp -i /etc/kubernetes/admin.conf .kube/config
[root@master01 ~]# ll .kube/
总用量 8
-rw------- 1 root root 5447 10月  1 12:32 config
```

### 5、pod网络部署

部署pod网络有两种方法利用calico部署、安装flannel 实现，在这里我们选择前者。值得注意的是==这一步的操作只需要在master节点操作即可==以下网址可以参考

calico部署

https://blog.csdn.net/qq_21816375/article/details/73694651

https://blog.csdn.net/u010801994/article/details/88715179

flannel部署

https://blog.csdn.net/qq_21816375/article/details/73691684

#### 5.1、利用calico部署

待写

#### 5.2 利用flannel部署

下载镜像，重打标签

因为yml文件连接被墙了，所以只能到别的地址下载好重新打标签。也可以改yml里面的地址。

```
[root@master01 ~]# docker pull easzlab/flannel:v0.11.0-amd64
v0.11.0-amd64: Pulling from easzlab/flannel
cd784148e348: Pull complete 
04ac94e9255c: Pull complete 
e10b013543eb: Pull complete 
005e31e443b1: Pull complete 
74f794f05817: Pull complete 
Digest: sha256:bd76b84c74ad70368a2341c2402841b75950df881388e43fc2aca000c546653a
Status: Downloaded newer image for easzlab/flannel:v0.11.0-amd64
[root@master01 ~]# docker tag easzlab/flannel:v0.11.0-amd64 quay.io/coreos/flannel:v0.11.0-amd64
[root@master01 ~]# docker rmi easzlab/flannel:v0.11.0-amd64
Untagged: easzlab/flannel:v0.11.0-amd64
Untagged: easzlab/flannel@sha256:bd76b84c74ad70368a2341c2402841b75950df881388e43fc2aca000c546653a
[root@master01 ~]# docker images
[root@master01 ~]# docker images
REPOSITORY                                                        TAG                 IMAGE ID            CREATED             SIZE
registry.aliyuncs.com/google_containers/kube-proxy                v1.17.2             cba2a99699bd        8 months ago        116MB
registry.aliyuncs.com/google_containers/kube-apiserver            v1.17.2             41ef50a5f06a        8 months ago        171MB
registry.aliyuncs.com/google_containers/kube-controller-manager   v1.17.2             da5fd66c4068        8 months ago        161MB
registry.aliyuncs.com/google_containers/kube-scheduler            v1.17.2             f52d4c527ef2        8 months ago        94.4MB
registry.aliyuncs.com/google_containers/coredns                   1.6.5               70f311871ae1        11 months ago       41.6MB
registry.aliyuncs.com/google_containers/etcd                      3.4.3-0             303ce5db0e90        11 months ago       288MB
quay.io/coreos/flannel                                            v0.11.0-amd64       ff281650a721        20 months ago       52.6MB
registry.aliyuncs.com/google_containers/pause                     3.1                 da86e6ba6ca1        2 years ago         742kB
[root@master01 ~]# 
```



```
[root@master01 ~]# vim kube-flannel.yml
添加下面的yml内容：
```

```
---
apiVersion: policy/v1beta1
kind: PodSecurityPolicy
metadata:
  name: psp.flannel.unprivileged
  annotations:
    seccomp.security.alpha.kubernetes.io/allowedProfileNames: docker/default
    seccomp.security.alpha.kubernetes.io/defaultProfileName: docker/default
    apparmor.security.beta.kubernetes.io/allowedProfileNames: runtime/default
    apparmor.security.beta.kubernetes.io/defaultProfileName: runtime/default
spec:
  privileged: false
  volumes:
    - configMap
    - secret
    - emptyDir
    - hostPath
  allowedHostPaths:
    - pathPrefix: "/etc/cni/net.d"
    - pathPrefix: "/etc/kube-flannel"
    - pathPrefix: "/run/flannel"
  readOnlyRootFilesystem: false
  # Users and groups
  runAsUser:
    rule: RunAsAny
  supplementalGroups:
    rule: RunAsAny
  fsGroup:
    rule: RunAsAny
  # Privilege Escalation
  allowPrivilegeEscalation: false
  defaultAllowPrivilegeEscalation: false
  # Capabilities
  allowedCapabilities: ['NET_ADMIN']
  defaultAddCapabilities: []
  requiredDropCapabilities: []
  # Host namespaces
  hostPID: false
  hostIPC: false
  hostNetwork: true
  hostPorts:
  - min: 0
    max: 65535
  # SELinux
  seLinux:
    # SELinux is unsed in CaaSP
    rule: 'RunAsAny'
---
kind: ClusterRole
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: flannel
rules:
  - apiGroups: ['extensions']
    resources: ['podsecuritypolicies']
    verbs: ['use']
    resourceNames: ['psp.flannel.unprivileged']
  - apiGroups:
      - ""
    resources:
      - pods
    verbs:
      - get
  - apiGroups:
      - ""
    resources:
      - nodes
    verbs:
      - list
      - watch
  - apiGroups:
      - ""
    resources:
      - nodes/status
    verbs:
      - patch
---
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1beta1
metadata:
  name: flannel
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: flannel
subjects:
- kind: ServiceAccount
  name: flannel
  namespace: kube-system
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: flannel
  namespace: kube-system
---
kind: ConfigMap
apiVersion: v1
metadata:
  name: kube-flannel-cfg
  namespace: kube-system
  labels:
    tier: node
    app: flannel
data:
  cni-conf.json: |
    {
      "name": "cbr0",
      "plugins": [
        {
          "type": "flannel",
          "delegate": {
            "hairpinMode": true,
            "isDefaultGateway": true
          }
        },
        {
          "type": "portmap",
          "capabilities": {
            "portMappings": true
          }
        }
      ]
    }
  net-conf.json: |
    {
      "Network": "172.16.0.0/16",
      "Backend": {
        "Type": "vxlan"
      }
    }
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds-amd64
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/arch: amd64
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.11.0-amd64
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.11.0-amd64
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
             add: ["NET_ADMIN"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
        - name: run
          hostPath:
            path: /run/flannel
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds-arm64
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/arch: arm64
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.11.0-arm64
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.11.0-arm64
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
             add: ["NET_ADMIN"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
        - name: run
          hostPath:
            path: /run/flannel
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds-arm
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/arch: arm
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.11.0-arm
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.11.0-arm
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
             add: ["NET_ADMIN"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
        - name: run
          hostPath:
            path: /run/flannel
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds-ppc64le
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/arch: ppc64le
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.11.0-ppc64le
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.11.0-ppc64le
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
             add: ["NET_ADMIN"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
        - name: run
          hostPath:
            path: /run/flannel
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg
---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: kube-flannel-ds-s390x
  namespace: kube-system
  labels:
    tier: node
    app: flannel
spec:
  selector:
    matchLabels:
      app: flannel
  template:
    metadata:
      labels:
        tier: node
        app: flannel
    spec:
      hostNetwork: true
      nodeSelector:
        beta.kubernetes.io/arch: s390x
      tolerations:
      - operator: Exists
        effect: NoSchedule
      serviceAccountName: flannel
      initContainers:
      - name: install-cni
        image: quay.io/coreos/flannel:v0.11.0-s390x
        command:
        - cp
        args:
        - -f
        - /etc/kube-flannel/cni-conf.json
        - /etc/cni/net.d/10-flannel.conflist
        volumeMounts:
        - name: cni
          mountPath: /etc/cni/net.d
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      containers:
      - name: kube-flannel
        image: quay.io/coreos/flannel:v0.11.0-s390x
        command:
        - /opt/bin/flanneld
        args:
        - --ip-masq
        - --kube-subnet-mgr
        resources:
          requests:
            cpu: "100m"
            memory: "50Mi"
          limits:
            cpu: "100m"
            memory: "50Mi"
        securityContext:
          privileged: false
          capabilities:
             add: ["NET_ADMIN"]
        env:
        - name: POD_NAME
          valueFrom:
            fieldRef:
              fieldPath: metadata.name
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        volumeMounts:
        - name: run
          mountPath: /run/flannel
        - name: flannel-cfg
          mountPath: /etc/kube-flannel/
      volumes:
        - name: run
          hostPath:
            path: /run/flannel
        - name: cni
          hostPath:
            path: /etc/cni/net.d
        - name: flannel-cfg
          configMap:
            name: kube-flannel-cfg

```

需要注意的是：=="Network": "172.16.0.0/16"要和初始化时的网段一致。==



部署网络并查看服务

```
[root@master01 ~]# kubectl apply -f kube-flannel.yml
podsecuritypolicy.policy/psp.flannel.unprivileged created
clusterrole.rbac.authorization.k8s.io/flannel created
clusterrolebinding.rbac.authorization.k8s.io/flannel created
serviceaccount/flannel created
configmap/kube-flannel-cfg created
daemonset.apps/kube-flannel-ds-amd64 created
daemonset.apps/kube-flannel-ds-arm64 created
daemonset.apps/kube-flannel-ds-arm created
daemonset.apps/kube-flannel-ds-ppc64le created
daemonset.apps/kube-flannel-ds-s390x created
[root@master01 ~]# kubectl get pod -n kube-system
NAME                               READY   STATUS    RESTARTS   AGE
coredns-9d85f5447-x8qxv            0/1     Pending   0          3h56m
coredns-9d85f5447-xsc6n            0/1     Pending   0          3h56m
etcd-master01                      1/1     Running   0          3h56m
kube-apiserver-master01            1/1     Running   0          3h56m
kube-controller-manager-master01   1/1     Running   0          3h56m
kube-flannel-ds-amd64-4259l        1/1     Running   0          50s
kube-proxy-l6fnj                   1/1     Running   0          3h56m
kube-scheduler-master01            1/1     Running   0          3h56m

```

服务必须全部Running

- pod的状态
- kube-system名称空间





```
[root@master01 ~]# kubectl get nodes
NAME       STATUS     ROLES    AGE     VERSION
master01   NotReady   master   4h24m   v1.17.2
work01     NotReady   <none>   8m14s   v1.17.2
work02     NotReady   <none>   8m3s    v1.17.2
[root@master01 ~]# kubectl get cs
NAME                 STATUS    MESSAGE             ERROR
controller-manager   Healthy   ok                  
scheduler            Healthy   ok                  
etcd-0               Healthy   {"health":"true"}   
[root@master01 ~]# kubectl cluster-info
Kubernetes master is running at https://10.10.30.40:6443
KubeDNS is running at https://10.10.30.40:6443/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

To further debug and diagnose cluster problems, use 'kubectl cluster-info dump'.
[root@master01 ~]# kubectl get pods --namespace kube-system
NAME                               READY   STATUS    RESTARTS   AGE
coredns-9d85f5447-x8qxv            0/1     Pending   0          4h26m
coredns-9d85f5447-xsc6n            0/1     Pending   0          4h26m
etcd-master01                      1/1     Running   2          4h26m
kube-apiserver-master01            1/1     Running   3          4h26m
kube-controller-manager-master01   1/1     Running   2          4h26m
kube-flannel-ds-amd64-4259l        1/1     Running   1          30m
kube-flannel-ds-amd64-744c2        1/1     Running   0          10m
kube-flannel-ds-amd64-zt578        1/1     Running   0          10m
kube-proxy-dzfhj                   1/1     Running   0          10m
kube-proxy-l6fnj                   1/1     Running   2          4h26m
kube-proxy-sg6n7                   1/1     Running   0          10m
kube-scheduler-master01            1/1     Running   2          4h26m
[root@master01 ~]# 

```

