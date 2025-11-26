# Linux运维的基础学习大纲

Linux运维的基础学习笔记

😒🤞❤💋💖😊😊😊😊😊🎁🎁🎁

## 第一阶段：Linux 入门基础（1-2 周）

学习目标：

* 理解 Linux 核心概念，掌握系统安装与基础操作，能独立完成日常命令使用

核心知识点：

1. Linux 概述

* 起源与发展（Unix 与 Linux 关系、主流发行版：CentOS、Ubuntu、Debian）
* Linux 优势与应用场景（服务器、嵌入式、云计算）

2. 系统安装与环境配置

* 虚拟机安装（VMware/VirtualBox）或双系统部署
* 图形界面（GNOME/KDE）与命令行界面（CLI）切换
* [远程连接工具使用](./linux/SSH远程连接工具使用推荐)（Xshell、SecureCRT、Putty）

3. 基础命令操作

* 目录与文件操作：cd、ls、pwd、mkdir、rm、cp、mv、touch、cat、more、less、head、tail
* 权限管理：chmod、chown、chgrp（理解 rwx 权限位、所有者 / 组 / 其他用户）
* 文件搜索：find、grep（正则表达式基础）
* 压缩与解压：tar、gzip、bzip2
* 系统信息查看：uname、hostname、df、du、free、top

## 第二阶段：Linux 核心技能（3-4 周）

学习目标：

* 掌握 Linux 系统核心配置、用户管理、进程与服务管理，具备基础运维能力

核心知识点：

1. 用户与组管理

* 用户创建 / 删除 / 修改（useradd、userdel、usermod）
* 组管理（groupadd、groupdel、groupmod）
* 密码管理（passwd、chage）
* sudo 权限配置（/etc/sudoers）

2. **[文件系统与磁盘管理](./linux/01.基础-必须掌握的命令/01.基础-必须掌握的命令)**

* Linux 文件系统结构（/bin、/etc、/home、/var 等目录作用）
* 磁盘分区（fdisk、parted）
* 挂载与卸载（mount、umount、/etc/fstab 配置）
* 文件系统格式化（mkfs.ext4、mkfs.xfs）

3. 进程与服务管理

* 进程查看与控制（ps、top、htop、kill、pkill）
* 服务管理（systemd、service 命令，/etc/systemd/system 配置）
* 后台进程与任务调度（nohup、&、crontab 定时任务）

4. 网络配置

* 网络接口配置（ifconfig、ip 命令）
* 静态 IP 与 DNS 配置（/etc/sysconfig/network-scripts、/etc/resolv.conf）
* 防火墙基础（firewalld、iptables 简单规则配置）
* 网络工具（ping、telnet、curl、wget、netstat、ss）

## 第三阶段：Linux 高级应用（4-6 周）

学习目标：

* 掌握 Shell 编程、软件编译安装、自动化运维工具，具备复杂场景处理能力

核心知识点：

1. Shell 编程基础

* [文本处理三剑客(grep-sed-awk)](.linux/01.基础-必须掌握的命令/03.文本处理三剑客grep-sed-awk/03.文本处理三剑客grep-sed-awk)
* Bash 脚本语法（变量、循环 for/while、条件判断 if/else、case）
* 函数与参数传递
* 脚本调试与优化（set -x、echo 调试）
* 常用脚本案例（文件备份、日志清理、系统监控）

1. 软件包管理

* RPM 包管理（rpm 命令安装 / 查询 / 卸载）
* YUM/DNF 仓库配置（本地仓库、网络仓库）
* 源码编译安装（configure、make、make install）

3. 日志与监控

* Linux 日志系统（/var/log 目录、rsyslog 配置）
* 日志分析工具（grep、awk、sed 基础）
* 系统监控工具（nmon、sar、iotop、iftop）

4. 自动化运维

* 远程批量操作（Ansible 基础：Inventory、Playbook）
* 配置文件同步（rsync 工具）

5. 安全加固

* SSH 安全配置（禁用 root 登录、修改默认端口、密钥登录）
* SELinux 配置（开启 / 关闭、模式切换）
* 恶意进程与日志审计

## 第四阶段：实战强化（按需拓展）

学习目标：

* 结合实际场景落地应用，巩固技能并拓展行业方向

实战场景：

1. 服务器搭建实战

* Web 服务器（Nginx/Apache 安装配置、虚拟主机、反向代理）
* 数据库服务器（MySQL/MariaDB 安装、用户授权、数据备份）
* FTP 服务器（vsftpd 配置）

2. 自动化脚本实战

* 企业级备份脚本（全量 + 增量备份、异地备份）
* 系统监控告警脚本（CPU / 内存 / 磁盘使用率告警）

3. 容器化与云计算

* Docker 基础（镜像 / 容器操作、Dockerfile 构建）
* Linux 与 K8s 基础（容器编排入门）

4. 行业方向拓展

* 运维方向：CI/CD（Jenkins）、监控平台（Zabbix）
* 开发方向：Linux 下编程环境配置（C/C++、Python）、项目部署
* 嵌入式方向：嵌入式 Linux 基础（裁剪、根文件系统构建）
