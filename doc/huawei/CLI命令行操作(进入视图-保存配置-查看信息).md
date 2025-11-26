# 03.CLI 命令行操作（进入视图、保存配置、查看信息）

# 华为 HCIE CLI 命令行核心操作指南（进入视图、保存配置、查看信息）

华为设备的 CLI（Command Line Interface）命令行操作遵循**分层视图结构**，核心操作围绕 “进入对应视图→配置 / 操作→保存配置→验证结果” 展开，以下是 HCIE 级别高频且核心的操作详解，覆盖通用设备（交换机、路由器、防火墙等）场景。

## 一、基础前提：登录设备与命令行模式概述

### 1. 登录方式（常见）

- Console 口登录：通过 Console 线连接设备 Console 口，终端软件（SecureCRT、Xshell）设置波特率 9600、数据位 8、停止位 1、无校验、无流控。
- 远程登录：SSH（推荐）或 Telnet，需提前配置管理 IP（如 VLANIF1），登录命令：`ssh 用户名@设备IP`​ 或 `telnet 设备IP`​。

### 2. 视图层级关系（核心！操作需先进入对应视图）

华为设备 CLI 分为 5 级视图，权限从低到高，命令作用范围逐步扩大：

|视图名称|进入命令|核心作用|权限级别|
| --------------| --------------------| ------------------------------------| ----------|
|用户视图|登录成功后直接进入|查看设备基础状态（非配置相关）|最低|
|系统视图|​`system-view`​（缩写：`sys`​）|全局配置（如主机名、管理 IP 等）|中级|
|接口视图|​`interface 接口类型 接口号`​|配置接口（IP、速率、VLAN 等）|中级|
|协议视图|如`ospf`​、`bgp`​、`vlan`​|配置特定协议（路由、VLAN 等）|高级|
|用户界面视图|​`user-interface [console/vty] 编号`​|配置登录方式（SSH/Telnet/Console）|中级|

## 二、核心操作 1：进入各类视图（含退出方法）

### 1. 进入用户视图（默认登录视图）

登录成功后直接进入，提示符为 `<>`​, 示例：

```bash
Huawei<>  # 用户视图提示符（设备默认主机名为Huawei）
```

### 2. 进入系统视图（全局配置入口）

从用户视图进入，是所有配置的 “总入口”，提示符为 `[]`​：

```bash
Huawei<> system-view  # 完整命令
Huawei<> sys          # 缩写（推荐，HCIE实操常用）
Enter system view, return user view with Ctrl+Z.  # 系统提示：按Ctrl+Z返回用户视图
[Huawei]  # 系统视图提示符
```

### 3. 进入接口视图（配置接口参数）

从系统视图进入，需指定**接口类型 + 接口号**（不同设备接口命名规则一致）：

#### 常见接口类型与示例：

- 以太网接口：`GigabitEthernet`​（千兆，缩写`GE`​）、`10GigabitEthernet`​（万兆，缩写`10GE`​）
- VLAN 接口：`Vlanif`​（三层交换机 / VPN 实例网关）
- 串口：`Serial`​（路由器广域网接口，缩写`S`​）
- 逻辑接口：`LoopBack`​（环回接口，用于测试 / 路由 ID）

#### 操作示例：

```bash
[Huawei] interface GigabitEthernet 0/0/1  # 进入千兆以太网接口0/0/1（0/0/1：槽位/子卡/端口）
[Huawei-GigabitEthernet0/0/1]  # 接口视图提示符（含接口名称）

[Huawei] interface Vlanif 10  # 进入VLAN 10的三层接口
[Huawei-Vlanif10]

[Huawei] interface LoopBack 0  # 进入环回接口0（常用作OSPF Router-ID）
[Huawei-LoopBack0]
```

### 4. 进入协议视图（配置路由 / 交换协议）

从系统视图进入，需指定协议名称（如 OSPF、BGP、VLAN、STP 等）：

#### 操作示例：

```bash
[Huawei] vlan batch 10 20 30  # 批量创建VLAN（直接在系统视图操作，无需单独协议视图）
[Huawei] ospf 1 router-id 1.1.1.1  # 进入OSPF进程1，指定Router-ID
[Huawei-ospf-1] area 0  # 进入OSPF区域0
[Huawei-ospf-1-area-0.0.0.0]

[Huawei] bgp 65001  # 进入BGP协议，AS号65001
[Huawei-bgp] peer 2.2.2.2 as-number 65002  # 配置BGP对等体
```

### 5. 退出视图的方法

- 从子视图返回上一级视图：`quit`​（缩写`q`​）

  ```bash
  [Huawei-GigabitEthernet0/0/1] quit  # 从接口视图返回系统视图
  [Huawei] quit  # 从系统视图返回用户视图
  Huawei<>
  ```
- 快速返回用户视图（任意视图）：`Ctrl+Z`​（快捷键，HCIE 实操高效操作）

  ```bash
  [Huawei-ospf-1-area-0.0.0.0] ^Z  # 按Ctrl+Z
  Huawei<>
  ```
- 退出 CLI 登录：`logout`​（用户视图执行）

  ```bash
  Huawei<> logout
  ```

## 三、核心操作 2：保存配置（避免配置丢失）

华为设备的配置分为两种：

- 临时配置（运行配置）：`running-config`​，仅在设备内存中，重启后丢失；
- 永久配置（启动配置）：`startup-config`​，保存在设备 Flash 中，重启后生效。

### 1. 保存当前配置（运行配置→启动配置）

**必须在用户视图或系统视图执行**，核心命令：

```bash
# 方法1：完整命令（推荐，明确保存路径）
Huawei<> save configuration to flash:/startup.cfg  # 保存到Flash默认启动文件
# 方法2：简化命令（最常用）
Huawei<> save  # 直接执行save，按提示确认
The current configuration will be written to the device.
Are you sure to continue? [Y/N]: y  # 输入y确认
It will take several seconds to save configuration file, please wait...
Configuration file has been saved successfully.  # 保存成功提示

# 系统视图也可执行
[Huawei] save
```

### 2. 覆盖已有启动配置（强制保存）

若启动配置已存在，需覆盖时，可直接指定文件名并加`force`​参数（避免交互确认）：

```bash
[Huawei] save flash:/startup.cfg force  # 强制覆盖原有启动配置，无交互
```

### 3. 关键验证：确认配置已保存

```bash
# 查看启动配置文件是否存在
Huawei<> dir flash:  # 列出Flash中的文件，需包含startup.cfg
Directory of flash:/

  1  -rw-    10240      Mar 10 2025 14:30:00  startup.cfg  # 存在则说明保存成功

# 对比运行配置与启动配置（确认是否一致）
[Huawei] display configuration difference  # 显示两者差异，无输出则一致
```

### 4. 注意事项（HCIE 易错点）

- 未保存配置时重启设备，所有临时配置丢失！建议配置完成后立即保存。
- 若需备份配置到 PC，可通过`FTP/SCP`​传输`startup.cfg`​文件。

## 四、核心操作 3：查看关键信息（验证配置 / 排障）

查看信息的命令需在对应视图执行，以下是 HCIE 高频查看命令，按场景分类：

### 1. 查看设备基础信息（用户视图 / 系统视图）

```bash
# 查看设备型号、版本、序列号（排障必备）
Huawei<> display version  # 缩写：dis ver
# 输出包含：设备型号（如S9306、AR6509）、VRP版本、序列号、硬件信息等

# 查看系统当前配置（运行配置）
[Huawei] display current-configuration  # 缩写：dis cur
# 查看指定模块的配置（高效，避免冗余输出）
[Huawei] display current-configuration interface GigabitEthernet 0/0/1  # 查看接口配置
[Huawei] display current-configuration ospf  # 查看OSPF配置

# 查看启动配置（重启后生效的配置）
[Huawei] display startup-configuration  # 缩写：dis startup
```

### 2. 查看接口状态与统计（任意视图）

```bash
# 查看所有接口的简要状态（UP/DOWN、IP、速率等）
Huawei<> display interface brief  # 缩写：dis int brief（最常用）
# 输出示例：
Interface                  PHY   Protocol  InUti OutUti   inErrors  outErrors
GigabitEthernet0/0/1       up    up         0%    0%          0         0
Vlanif10                   up    up         0%    0%          0         0

# 查看指定接口的详细信息（协商模式、流量统计、错误包等）
Huawei<> display interface GigabitEthernet 0/0/1  # 缩写：dis int GigabitEthernet 0/0/1
# 重点关注：Physical status（物理状态）、Protocol status（协议状态）、IP address、Input/Output packets
```

### 3. 查看协议相关信息（协议视图 / 系统视图）

#### （1）路由协议信息（OSPF/BGP）

```bash
# 查看OSPF邻居表
[Huawei-ospf-1] display ospf peer  # 缩写：dis ospf peer
# 查看OSPF路由表
[Huawei] display ospf routing  # 缩写：dis ospf routing

# 查看BGP对等体状态
[Huawei-bgp] display bgp peer  # 缩写：dis bgp peer
# 查看BGP路由表
[Huawei] display bgp routing-table  # 缩写：dis bgp routing-table
```

#### （2）VLAN/STP 信息（交换机常用）

```bash
# 查看VLAN配置
[Huawei] display vlan brief  # 查看所有VLAN的端口归属
[Huawei] display vlan 10  # 查看VLAN 10的详细信息

# 查看STP状态（生成树协议）
[Huawei] display stp  # 查看全局STP信息（根桥、优先级等）
[Huawei] display stp interface GigabitEthernet 0/0/1  # 查看接口STP状态
```

### 4. 查看设备资源与性能（用户视图 / 系统视图）

```bash
# 查看CPU利用率（排障高负载问题）
Huawei<> display cpu-usage  # 缩写：dis cpu-usage
# 查看内存利用率
Huawei<> display memory-usage  # 缩写：dis memory-usage

# 查看日志信息（排障必备）
Huawei<> display logbuffer  # 查看缓存日志（最近的系统事件）
[Huawei] display trapbuffer  # 查看告警日志
```

## 五、HCIE 实操技巧（提升效率）

1. **命令缩写**：华为 CLI 支持命令前几位唯一匹配缩写（如`sys`​\=system-view、`dis`​\=display、`int`​\=interface），实操中优先使用缩写。
2. **命令补全**：按`Tab`​键自动补全命令 / 接口名（如输入`int G0/0/`​后按 Tab，自动补全接口号）。
3. **历史命令**：按`↑`​键调用之前执行的命令，避免重复输入。
4. **过滤输出**：使用`| include`​过滤关键信息（如`dis cur | include ip address`​，只显示包含 IP 地址的配置）。
5. **批量配置**：系统视图执行`batch-run`​批量导入命令，或使用`copy configuration`​复制配置。

## 总结

华为 HCIE CLI 核心操作逻辑：**登录→进入对应视图（配置 / 操作）→保存配置→查看信息验证**。关键在于熟练掌握视图层级切换、`save`​命令的使用，以及针对性的查看命令（如排障用`display logbuffer`​、验证路由用`display ospf routing`​）。实操中需注意命令缩写和快捷键的使用，提升配置效率。

‍
