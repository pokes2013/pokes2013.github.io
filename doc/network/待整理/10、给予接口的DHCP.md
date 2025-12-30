# 07.给予接口的DHCP

‍

```python
interface Vlanif10
 ip address 10.5.1.1 255.255.255.0
 dhcp select interface
 dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378
 dhcp server excluded-ip-address 10.5.1.200 10.5.1.254
 dhcp server lease day 0 hour 0 minute 5
 dhcp server dns-list 114.114.114.114
```

‍

interface Vlanif10

#vlan地址

ip address 10.5.1.1 255.255.255.0

#选择基于接口的dhcp类型

dhcp select interface

#绑定MAC静态IP

dhcp server static-bind ip-address 10.5.1.100 mac-address 5489-98b7-7378

#排除保留的地址

dhcp server excluded-ip-address 10.5.1.200 10.5.1.254

#设置租约

dhcp server lease day 0 hour 0 minute 5

#配置DNS

dhcp server dns-list 114.114.114.114  

‍
