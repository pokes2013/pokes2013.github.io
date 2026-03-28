# Ubuntu2024换国内源

‍

Ubuntu24.04的源地址配置文件发生改变，不再使用以前的sources.list文件，升级24.04之后，而是使用如下文件

```shell
/etc/apt/sources.list.d/ubuntu.sources
```

‍

换源

```shell
sudo cp /etc/apt/sources.list.d/ubuntu.sources  /etc/apt/sources.list.d/ubuntu.sources.bak

sudo vim /etc/apt/sources.list.d/ubuntu.sources


添加以下内容：
Types: deb
URIs: http://mirrors.tuna.tsinghua.edu.cn/ubuntu/
Suites: noble noble-updates noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg


sudo apt-get update
sudo apt-get upgrade

```

‍
