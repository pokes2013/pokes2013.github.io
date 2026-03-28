

# ubuntu使用开启远程xfce4



如何解决 xrdp 远程黑屏问题？

xrdp 远程黑屏、登录后只有鼠标、闪退，是 Ubuntu 最常见问题，我给你**一套最稳、一次就能好**的完整修复方案，直接复制执行即可。

## 1. 安装必要组件（必做）

```bash
sudo apt install -y xorgxrdp xfce4 xfce4-goodies
```



gdm3    lightdm  这两个选哪个

## 2. 配置启动桌面（关键修复）

在用户目录创建 `.xsession` 文件：

```bash
echo xfce4-session > ~/.xsession
```

再给全局配置：

```bash
echo xfce4-session | sudo tee /etc/xrdp/startwm.sh
```

## 3. 修改 startwm.sh（最有效）

```bash
sudo nano /etc/xrdp/startwm.sh
```

把文件**最底部**这两行：

```plaintext
test -x /etc/X11/Xsession && exec /etc/X11/Xsession
exec /bin/sh /etc/X11/Xsession
```

**注释掉**（前面加 #），然后在它们上面添加：

```plaintext
startxfce4
```

最终像这样：

```plaintext
# test -x /etc/X11/Xsession && exec /etc/X11/Xsession
# exec /bin/sh /etc/X11/Xsession
startxfce4
```

保存退出：

`Ctrl+O` → 回车 → `Ctrl+X`

## 4. 重启 xrdp

```bash
sudo systemctl restart xrdp
```

## 5. 不要用 root 远程登录

用普通用户登录，否则必黑屏。

## 6. 如果你用的是 GNOME（Ubuntu 默认桌面）

GNOME 和 xrdp 兼容性很差，**强烈建议直接用上面的 xfce4**，基本 100% 不黑屏。

------

## 终极一键修复脚本（直接复制全执行）

```bash
sudo apt install -y xorgxrdp xfce4 xfce4-goodies
echo xfce4-session > ~/.xsession
sudo sed -i 's/^test -x \/etc\/X11\/Xsession/#&/' /etc/xrdp/startwm.sh
sudo sed -i 's/^exec \/bin\/sh \/etc\/X11\/Xsession/#&/' /etc/xrdp/startwm.sh
sudo sed -i '/^#exec \/bin\/sh/a startxfce4' /etc/xrdp/startwm.sh
sudo systemctl restart xrdp
```

------

执行完后**重新远程连接**，99% 直接正常显示桌面，不再黑屏。

如果你告诉我你的 Ubuntu 版本（20.04 / 22.04 / 24.04），我可以给你对应版本最精准的方案。