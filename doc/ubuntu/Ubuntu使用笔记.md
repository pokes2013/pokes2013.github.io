



## 简单挂载

直接在命令中输入密码（简单，但密码明文显示在历史中）

**请将 `your_username` 和 `your_password` 替换为你的Windows用户名和密码。**

```
sudo mount -t cifs -o username=pokes,password=123456,uid=1000,gid=1000,iocharset=utf8 //192.168.1.141/09-erp系统 /mnt/ligong141
```

**参数解释：**

- `-t cifs`: 指定文件系统类型为CIFS（Windows共享协议）。
- `-o`: 后面跟着挂载选项。
- `username=...`, `password=...`: Windows系统的登录用户名和密码。
- `uid=1000`, `gid=1000`: 确保挂载后的文件所有者是你的Ubuntu用户（通常第一个用户的ID是1000），这样你才有读写权限。
- `iocharset=utf8`: 保证中文文件名能正确显示。
- `//192.168.1.141/Share`: Windows共享的网络路径。
- `/mnt/ligong141`: 你刚刚创建的本地挂载点。

### 验证是否挂载成功

```bash
df -hT

pokes@pokes-VMware-Virtual-Platform:~$ df -hT
文件系统                   类型   大小  已用  可用 已用% 挂载点
tmpfs                      tmpfs  790M  2.4M  788M    1% /run
/dev/sda2                  ext4   511G   19G  466G    4% /
tmpfs                      tmpfs  3.9G  700M  3.2G   18% /dev/shm
tmpfs                      tmpfs  5.0M  8.0K  5.0M    1% /run/lock
tmpfs                      tmpfs  790M  148K  790M    1% /run/user/1000
//192.168.1.141/09-erp系统 cifs   163G   58G  106G   36% /mnt/ligong141

```



### 设置开机自动挂载

如果你希望每次开机都自动挂载这个共享，需要编辑 `/etc/fstab` 文件。

1. **备份并编辑文件**：

   bash

   ```
   sudo cp /etc/fstab /etc/fstab.backup
   sudo nano /etc/fstab
   ```

   

2. **在文件末尾添加一行**（使用方法B的凭据文件方式）：

   text

   ```
   //192.168.1.141/Share/mnt/ligong141  cifs  credentials=/home/你的用户名/.smbcredentials_ligong141,uid=1000,gid=1000,iocharset=utf8,_netdev,nofail  0  0
   ```

   

   **重要选项说明：**

   - `_netdev`: 告知系统这是一个网络设备，等网络准备好之后再尝试挂载。
   - `nofail`: 如果挂载失败（例如Windows关机了），系统不会因此卡住启动过程而进入紧急模式。**这个选项非常重要！**

3. **测试配置是否正确**（在重启前必须做！）：

   bash

   ```
   sudo mount -a
   ```

   

   这条命令会尝试挂载所有在 `fstab` 中定义的文件系统。如果没有报错，说明你的配置写对了。

### 卸载命令

当你不需要使用时，可以手动卸载：

bash

```
sudo umount /mnt/ligong141
```



现在，你就可以像访问本地文件夹一样访问 `/mnt/ligong141` 里的内容了。





```
su root
useradd anita					# 在系统中添加一个名为anita的普通用户
pdbedit -a -u anita001			# 创建一个名为anita001的samba用户，其后会提示输入两次密码
mkdir -p /home/pokes/public	    # 创建一个用于共享的目录

chown anita001:anita001 /home/noSmileCat/share		# 设置共享目录所属组跟用户
```



### 配置samba服务器

配置文件：/etc/samba/smb.conf
配置文件中有许多注释，可通过下面命令去掉注释

```
su root
mv /etc/samba/smb.conf /etc/samba/smb.conf.bak
cat /etc/samba/smb.conf.bak | grep -v "#" | grep -v ";" | grep -v "^$" > /etc/samba/smb.conf
cat /etc/samba/smb.conf
```



```
[Public]
   comment = Public File Share
   path = /home/pokes/Public
   browsable = yes
   read only = no
   guest ok = yes
   create mask = 0664
   directory mask = 0775
```



cat /etc/samba/smb.conf | grep -v "#" | grep -v ";" | grep -v "^$" >> pokes.txt



> Samba 用户信息存储在特定的数据库文件中（默认为 `tdbsam`），你可以使用 `tdbtool` 来查看这个文件的内容。这种方法更底层。
>
> sudo tdbtool /var/lib/samba/private/passdb.tdb list
>
> **注意**：数据库文件路径可能是 `/var/lib/samba/passdb.tdb`，具体取决于你的 Samba 版本和配置。`pdbedit -L` 是更安全简单的选择。

创建Samba用户

```
dbedit -a -u pokes1
```

查看Samba用户

```
sudo pdbedit -L	     #简易版信息
sudo pdbedit -L -v   #更详细的信息
```

修改密码

smbpasswd 命令主要用于修改密码，但也可以用来查看用户是否存在。

```
sudo smbpasswd -a anita   #添加一个新的 Samba 用户并为其设置密码。
sudo smbpasswd -e 用户名   #启用一个已被禁用的 Samba 用户账户。
```

### 常用管理命令（不只是查看）

了解了查看命令，这里还有一些相关的常用管理命令：

| 命令                        | 功能                              | 示例                       |
| :-------------------------- | :-------------------------------- | :------------------------- |
| `sudo pdbedit -L`           | **列出所有Samba用户**             | `sudo pdbedit -L`          |
| `sudo pdbedit -L -v`        | **列出所有Samba用户的详细信息**   | `sudo pdbedit -L -v`       |
| `sudo smbpasswd -a 用户名`  | **添加一个系统用户到Samba数据库** | `sudo smbpasswd -a pokes`  |
| `sudo smbpasswd -e 用户名`  | **启用一个Samba用户**             | `sudo smbpasswd -e pokes`  |
| `sudo smbpasswd -d 用户名`  | **禁用一个Samba用户**             | `sudo smbpasswd -d pokes`  |
| `sudo smbpasswd -x 用户名`  | **从Samba数据库中删除一个用户**   | `sudo smbpasswd -x pokes`  |
| `sudo pdbedit -r -u 用户名` | **修改用户的Samba账户信息**       | `sudo pdbedit -r -u pokes` |



### 总结

- 要快速查看有哪些用户能通过 Samba 登录，**首选命令是 `sudo pdbedit -L`**。
- 要查看某个用户的详细账户信息，使用 `sudo pdbedit -L -v | grep -A 20 "Unix username: pokes"`（将 `pokes` 替换为你要查找的用户名）。
- 记住，Samba 用户的前提是**必须已经是 Linux 系统用户**。`pdbedit -L` 列表中的用户都在 `/etc/passwd` 文件中存在。

现在你可以轻松地查看和管理你的 Samba 用户了。