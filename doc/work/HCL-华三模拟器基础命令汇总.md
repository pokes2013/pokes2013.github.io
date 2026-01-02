# HCL-华三模拟器基础命令汇总



## 设备改名

```
[H3C]sysname sw1
```



## VLAN

```bash
[Sysname] vlan 2
[Sysname-vlan2] quit
[Sysname] interface GigabitEthernet3/0/24
[Sysname-GigabitEthernet3/0/24] port access vlan 2
[Sysname-GigabitEthernet3/0/24] quit

[Sysname] interface Vlan-interface 2
[Sysname-Vlan-interface2] ip address 192.168.1.50 24
```



## Console口登录

主机通过配置电缆与设备的Console口连接。现要求：用户通过设备的Console口登录到设备，对设备进行管理和配置，并且配置本地认证方式为AAA认证，以提高设备的安全性。



配置思路

- 通过Console口登录设备，需要使用户终端的通信参数配置和交换机Console口的缺省配置保持一致。

- 当通过Console口采用本地认证方式登录时，由于本地用户缺省的授权用户角色为network-operator，且本地是无服务类型的。因此，需要设置本地用户的服务类型为terminal（通过Console口登录使用的是terminal服务类型），授权用户角色为network-admin，才能使用户下次成功登录并在登录后对设备进行管理和配置。



配置步骤

- 主机断电。因为PC机串口不支持热插拔，请不要在PC带电的情况下，将配置电缆插入或者拔出PC机。

- 请使用产品随机附带的配置电缆连接PC机和设备。请先将配置口电缆的DB-9（孔）插头插入PC机的9芯（针）串口中，再将RJ-45插头端插入设备的Console口中。

## 开启Telnet

可能有问题，需要进一步验证

```
# 通过Console口登录设备，进入系统视图，开启Telnet服务。

<Sysname> system-view
[Sysname] telnet server enable

# 设置通过VTY用户线登录交换机使用AAA的认证方式。

[Sysname] line vty 0 63
[Sysname-line-vty0-63] authentication-mode scheme
[Sysname-line-vty0-63] quit

# 创建本地用户userA，授权其用户角色为network-admin，为其配置密码，删除默认角色。

[Sysname] local-user userA class manage

New local user added.

[Sysname-luser-manage-userA] authorization-attribute user-role network-admin
[Sysname-luser-manage-userA] service-type telnet
[Sysname-luser-manage-userA] password simple 123
[Sysname-luser-manage-userA] undo authorization-attribute user-role network-operator
[Sysname-luser-manage-userA] quit

# 创建用户角色roleB，权限为允许执行所有特性中读类型的命令。

[Sysname] role name roleB
[Sysname-role-roleB] rule 1 permit read feature
[Sysname-role-roleB] quit

# 创建本地用户userB，为其配置密码，授权其用户角色为roleB，删除默认角色。

[Sysname] local-user userB class manage
New local user added.
[Sysname-luser-manage-userB] authorization-attribute user-role roleB
[Sysname-luser-manage-userB] service-type telnet
[Sysname-luser-manage-userB] password simple 123
[Sysname-luser-manage-userB] undo authorization-attribute user-role network-operator
[Sysname-luser-manage-userB] quit

# 创建ACL视图，定义规则，仅允许来自192.168.0.46和192.168.0.52的用户访问交换机。

[Sysname] acl number 2000
[Sysname-acl-basic-2000] rule 1 permit source 192.168.0.46 0
[Sysname-acl-basic-2000] rule 2 permit source 192.168.0.52 0
[Sysname-acl-basic-2000] rule 3 deny source any
[Sysname-acl-basic-2000] quit

# 引用访问控制列表2000，通过源IP对Telnet用户进行控制。

[Sysname] telnet server acl 2000
```

###### 
