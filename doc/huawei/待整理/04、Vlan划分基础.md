# Vlan划分基础

## 基于接口划分VLAN（重点掌握）

长时间不用就会忘记，多敲敲就会记住。

```go
[sw1]int g0/0/1
[sw1-GigabitEthernet0/0/1]port link-type access 
[sw1-GigabitEthernet0/0/1]port default vlan 10
[sw1-GigabitEthernet0/0/1]q
```

## 基于MAC地址的VLAN（不推荐）

后期工作量太大

‍

## 基于IP子网划分 VLAN（重点）

![image](image-20241125191410-f6delkw.png)

sw2

```go
<Huawei>sys
[Huawei]sysname sw2
[sw2]

[sw2]un in en    #关闭消息回执
Info: Information center is disabled.

[sw2]vlan batch 10 20

[sw2]int g0/0/2
[sw2-GigabitEthernet0/0/2]port link-type access 
[sw2-GigabitEthernet0/0/2]port default vlan 10
[sw2-GigabitEthernet0/0/2]q
[sw2]int g0/0/3
[sw2-GigabitEthernet0/0/3]port link-type access 
[sw2-GigabitEthernet0/0/3]port default vlan 20
[sw2-GigabitEthernet0/0/3]q
[sw2]dis vlan
The total number of vlans is : 3
--------------------------------------------------------------------------------
U: Up;         D: Down;         TG: Tagged;         UT: Untagged;
MP: Vlan-mapping;               ST: Vlan-stacking;
#: ProtocolTransparent-vlan;    *: Management-vlan;
--------------------------------------------------------------------------------

VID  Type    Ports                                                        
--------------------------------------------------------------------------------
1    common  UT:GE0/0/1(U)      GE0/0/4(D)      GE0/0/5(D)      GE0/0/6(D)    
                GE0/0/7(D)      GE0/0/8(D)      GE0/0/9(D)      GE0/0/10(D)   
                GE0/0/11(D)     GE0/0/12(D)     GE0/0/13(D)     GE0/0/14(D)   
                GE0/0/15(D)     GE0/0/16(D)     GE0/0/17(D)     GE0/0/18(D)   
                GE0/0/19(D)     GE0/0/20(D)     GE0/0/21(D)     GE0/0/22(D)   
                GE0/0/23(D)     GE0/0/24(D)                                   

10   common  UT:GE0/0/2(U)                                                    

20   common  UT:GE0/0/3(U)                                                    


VID  Status  Property      MAC-LRN Statistics Description    
--------------------------------------------------------------------------------

1    enable  default       enable  disable    VLAN 0001                       
10   enable  default       enable  disable    VLAN 0010                       
20   enable  default       enable  disable    VLAN 0020                       
[sw2]

[sw2]int g0/0/1
[sw2-GigabitEthernet0/0/1]port link-type trunk 
[sw2-GigabitEthernet0/0/1]port trunk allow-pass vlan 10 20


```

sw1

```go
The device is running!

<Huawei>
<Huawei>sys
Enter system view, return user view with Ctrl+Z.
[Huawei]sysn
[Huawei]sysname sw1
[sw1]
[sw1]
[sw1]int g0/0/2
[sw1]un in en
[sw1]int g0/0/2
[sw1-GigabitEthernet0/0/2]port link-type trunk 
[sw1-GigabitEthernet0/0/2]port trunk allow-pass vlan 10 20
[sw1-GigabitEthernet0/0/2]q

[sw1]vlan batch 10 20
[sw1]vlan 10
[sw1-vlan10]mac-vlan mac-address 0000-0000-0001
[sw1-vlan10]q

[sw1]vlan 20
[sw1-vlan20]mac-vlan mac-address 0000-0000-0002
[sw1-vlan20]q

[sw1]int g0/0/1
[sw1-GigabitEthernet0/0/1]port hybrid untagged vlan 10 20	#让g0/01属于多个vlan
[sw1-GigabitEthernet0/0/1]mac-vlan enable    #开启基于mac的学习vlan

[sw1]dis vlan
The total number of vlans is : 3
--------------------------------------------------------------------------------
U: Up;         D: Down;         TG: Tagged;         UT: Untagged;
MP: Vlan-mapping;               ST: Vlan-stacking;
#: ProtocolTransparent-vlan;    *: Management-vlan;
--------------------------------------------------------------------------------

VID  Type    Ports                                                        
--------------------------------------------------------------------------------
1    common  UT:GE0/0/1(U)      GE0/0/2(U)      GE0/0/3(D)      GE0/0/4(D)    
                GE0/0/5(D)      GE0/0/6(D)      GE0/0/7(D)      GE0/0/8(D)    
                GE0/0/9(D)      GE0/0/10(D)     GE0/0/11(D)     GE0/0/12(D)   
                GE0/0/13(D)     GE0/0/14(D)     GE0/0/15(D)     GE0/0/16(D)   
                GE0/0/17(D)     GE0/0/18(D)     GE0/0/19(D)     GE0/0/20(D)   
                GE0/0/21(D)     GE0/0/22(D)     GE0/0/23(D)     GE0/0/24(D)   

10   common  UT:GE0/0/1(U)                                                    

             TG:GE0/0/2(U)                                                    

20   common  UT:GE0/0/1(U)                                                    

             TG:GE0/0/2(U)                                                    


VID  Status  Property      MAC-LRN Statistics Description    
--------------------------------------------------------------------------------

1    enable  default       enable  disable    VLAN 0001                       
10   enable  default       enable  disable    VLAN 0010                       
20   enable  default       enable  disable    VLAN 0020                       
[sw1]

```

说明：tag可以称为带标签的数据帧，所以untag即为不带标签；tagged为带标签发送，untagged为去掉标签后发送。上面这行port hybrid untagged vlan 10 20 的意思是让端口属于vlan10和20，发送数据帧时不打标签。
