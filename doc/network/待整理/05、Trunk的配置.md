# 02.Trunk的配置

华为交换机的 Trunk 配置主要用于在交换机之间传输多个 VLAN 的数据。以下是华为交换机 Trunk 端口的基本配置步骤：

​```
```bash
port link-type trunk
​port trunk allow-pass vlan all​
​port trunk allow-pass vlan 10 20 30
```

‍

‍

‍
