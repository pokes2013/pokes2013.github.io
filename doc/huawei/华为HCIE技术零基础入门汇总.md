# 华为HCIE技术零基础入门汇总



我目前从事网络运维相关工作，😂😂日常工作的核心聚焦在路由与交换技术的实操与保障上。由于岗位业务场景的特殊性，平时处理的大多是局域网内的设备配置、链路优化、故障排查等事务 —— 比如路由器静态路由与动态路由协议（如 OSPF、RIP）的调试与维护，交换机 VLAN 划分、 trunk 链路配置、端口聚合与风暴抑制等核心操作，这些都是日常工作中高频接触的内容，也是保障内网稳定运行的关键环节。🤞🤞🤞❤❤❤

基于工作中的实际需求，我在整理相关技术文档、操作手册或经验分享时，会把路由与交换这部分经常用到的知识点、实操步骤、常见问题解决方案写得更细致、更具体，比如会详细标注不同场景下的配置命令差异、故障排查的排查思路与步骤拆解，方便自己后续查阅，也希望能给有需要的同事提供更具参考价值的内容。
不过由于工作中涉及外网技术的场景相对较少，相关的实操经验和整理内容会相对简略一些。如果大家在阅读过程中发现有不够全面的地方，或者对内容有其他建议、需求，欢迎随时和我沟通交流，也请大家多多包涵！😎😎😁😁😁

## 一、计算机网络基础

1. [IP地址原理及分类](https://blog.csdn.net/weixin_42132035/article/details/142319542)

2. [子网划分详解与实例](https://blog.csdn.net/wj31932/article/details/127939596)

3. [OSI 七层模型与 TCP／IP 协议栈](https://pokes.blog.csdn.net/article/details/109101643)

4. [常用网络命令（ping、tracert、ipconfig）](https://blog.csdn.net/weixin_64122448/article/details/123248119)

## 二、交换机部分

[首次Console口登陆配置Telnet访问](https://pokes.blog.csdn.net/article/details/112971589)

### 2.1、VLAN

1. [VLAN的介绍、单交换机vlan划分实验](https://pokes.blog.csdn.net/article/details/109130709)
2. [多交换机划分vlan——trunk的配置](https://pokes.blog.csdn.net/article/details/112983355)

3. [批量配置端口——端口组](https://blog.csdn.net/annita2019/article/details/109132399)
4. [基于IP子网划分 VLAN](https://blog.csdn.net/annita2019/article/details/109558187)
5. [基于MAC地址划分VLAN](https://pokes.blog.csdn.net/article/details/109489089)
6. [三层交换机实现vlan间通信](https://blog.csdn.net/annita2019/article/details/109195314)
7. [三层交换机企业组网实例](https://blog.csdn.net/annita2019/article/details/109240641)

### 2.2、ARP
1. [ARP代理实现同网段不同vlan通信](https://pokes.blog.csdn.net/article/details/124425702)
2. [ARP静态绑定技术](https://blog.csdn.net/annita2019/article/details/126347820)

### 2.3、交换机技术
1. [STP（生成树协议）技术原理与工作机制详解（面试重点）](https://blog.csdn.net/annita2019/article/details/126162123)
2. [STP的详解和试验](https://pokes.blog.csdn.net/article/details/132810044)
3. [STP的高级技术边缘端口、BPDU保护](https://blog.csdn.net/annita2019/article/details/132810044)
4. [RSTP快速生成树协议深度剖析：结合华为eNSP模拟器的完整实验方案](https://blog.csdn.net/annita2019/article/details/148808913)
5. [MSTP的基础配置](https://blog.csdn.net/annita2019/article/details/132824544)
6. [Eth-Trunk链路聚合技术](https://blog.csdn.net/annita2019/article/details/109716902)
7. [交换机端口镜像技术](https://blog.csdn.net/annita2019/article/details/109692243)

### 2.4、DHCP技术

1. [DHCP原理及基础配置实验](https://blog.csdn.net/annita2019/article/details/109582359)
2. [三层交换机基于接口的DHCP](https://blog.csdn.net/annita2019/article/details/118639767)
3. [VLAN间互通+DHCP中继组网实例](https://blog.csdn.net/annita2019/article/details/112607189)
4. [企业VLAN间通讯及DHCP中继（中继Server2008DHCP服务器）](https://blog.csdn.net/annita2019/article/details/124699699)

## 三、路由器部分
### 基础技术
1. [首次登陆配置Console、Telnet登录、Web登录](https://blog.csdn.net/annita2019/article/details/109646522)
2. [AR1200真机忘记Console口密码的处理方法全过程演示](https://blog.csdn.net/annita2019/article/details/109365707)
3. [静态路由实现跨网段](https://blog.csdn.net/annita2019/article/details/109135373)
4. [默认路由](https://blog.csdn.net/annita2019/article/details/109223257)
5. [NAT地址转换技术](https://blog.csdn.net/annita2019/article/details/109672507)
6. [ACL介绍及配置实验](https://blog.csdn.net/annita2019/article/details/110994409)
7. [路由策略](https://blog.csdn.net/annita2019/article/details/153814748)
8. [策略路由](https://blog.csdn.net/2401_85549756/article/details/139525169)
9. [PPPOE配置模拟实验及NAT配置](https://blog.csdn.net/annita2019/article/details/118767844)
10. [PPPoE结合虚拟机的模拟实验（含NAT）](https://blog.csdn.net/annita2019/article/details/118713303)
11. [华为路由器ppp协议](https://blog.csdn.net/annita2019/article/details/109198595)
12. [虚拟路由冗余协议VRRP的讲解](https://blog.csdn.net/annita2019/article/details/114067753)
13. [VRRP+MSTP典型组网配置](https://blog.csdn.net/annita2019/article/details/114295521)
14. [华为路由器ppp协议](https://blog.csdn.net/annita2019/article/details/109198595)
15. [loopback（本地回环）接口的作用](https://blog.csdn.net/annita2019/article/details/109523858)
16. [单臂路由实验](https://blog.csdn.net/annita2019/article/details/109143614)
17. [静态路由与BFD联动实现主备切换](https://blog.csdn.net/annita2019/article/details/109626979)
18. [动态路由协议——RIP协议](https://blog.csdn.net/annita2019/article/details/109152291)


## WLAN
1. [AP上线的基本配置](https://blog.csdn.net/zzaizhu/article/details/135035648)
2. [AP上线之旁挂二层直接转发AP无认证](https://blog.csdn.net/weixin_45605234/article/details/137352360)
## 防火墙技术
1. [防火墙的介绍及基本配置](https://blog.csdn.net/annita2019/article/details/109788727)
2. [SLB基于服务器的负载均衡](https://blog.csdn.net/annita2019/article/details/109803203)


## OSPF（重点）
1. [OSPF协议协议介绍及概念部分](https://blog.csdn.net/annita2019/article/details/109152646)
2. [OSPF协议三张表及邻居建立过程，常见故障的解决方法](https://blog.csdn.net/annita2019/article/details/109519906)
3. [OSPF单区域实验](https://blog.csdn.net/annita2019/article/details/119064992)
4. [多区域OSPF协议实验](https://blog.csdn.net/annita2019/article/details/109511867)
5. [十分钟理解OSPF路由协议(OSPF概念的总结)](https://blog.csdn.net/annita2019/article/details/133011513)

## ISIS中间系统到中间系统

[ISIS基本原理与配置（含实验）](https://blog.csdn.net/annita2019/article/details/125877265)

## BGP

