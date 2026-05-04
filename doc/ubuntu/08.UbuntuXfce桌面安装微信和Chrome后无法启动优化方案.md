

# Ubuntu Xfce 桌面安装微信、Chrome 后无法启动优化方案



## 第一节：xfce桌面微信最小化问题



xfce桌面,微信就直接最小化 / 隐藏了，窗口没了但进程还在跑，再点图标也唤不出来，这是微信客户端的 “关闭行为” 问题。下面给你一套完整、一次性解决的方案，既能让它点叉号时只最小化到托盘不退出，又能保证图标能正常唤回窗口。

### 一、先确认微信的真实启动命令

先在终端运行一下，确认你用的是哪个版本：

```bash
# 试一下这两个命令，哪个能启动就用哪个

which wechat
which electronic-wechat
```

比如输出是 /usr/bin/wechat 或 /usr/bin/electronic-wechat，记下来。

### 二、修改桌面快捷方式，实现 “点叉不退出，托盘唤回”

1. 重新创建正确的桌面文件（适配你的中文桌面）
  把下面这段复制到终端，一次性运行：

  ```bash
  cat > ~/桌面/wechat.desktop << 'EOF'
  [Desktop Entry]
  Version=1.0
  Name=微信
  Comment=微信客户端
  # 这里的Exec=后面，根据你上面which的结果修改
  Exec=bash -c "pgrep -x wechat && wmctrl -xa 'WeChat' || wechat --minimize-to-tray"
  Icon=wechat
  Terminal=false
  Type=Application
  Categories=Network;InstantMessaging;
  StartupWMClass=WeChat
  EOF
  ```

  > 如果你的命令是 electronic-wechat，把上面的 wechat 改成 electronic-wechat 即可。
2. 赋予可执行权限

  ```bash
  chmod +x ~/桌面/wechat.desktop
  ```

### 三、关键：让 XFCE 面板显示微信托盘图标

你之前点叉号微信就 “消失”，是因为**右下角没有托盘区域，看不到微信图标**，自然唤不出来。

```bash
sudo apt install -y wmctrl libayatana-appindicator3-1 xfce4-indicator-plugin
```

然后重启

```bash
# 重启任务栏
xfce4-panel -r
# 有时候重启没起来
xfce4-panel &
# 合并两行代码
xfce4-panel -r &&  xfce4-panel &
```

### 四、更好的办法

```bash
# 先创建目录（如果不存在）
mkdir -p ~/.local/bin

# 写入脚本
cat > ~/.local/bin/wechat-start.sh << 'EOF'
#!/bin/bash

# 1. 设置输入法环境变量（解决中文输入问题）
export GTK_IM_MODULE=fcitx5
export QT_IM_MODULE=fcitx5
export XMODIFIERS=@im=fcitx5

# 2. 尝试唤回已有的微信窗口（如果微信在后台）
wmctrl -xa "WeChat"

# 3. 如果没有唤回成功（说明微信没运行），就启动微信
if [ $? -ne 0 ]; then
    wechat --minimize-to-tray
fi
EOF

# 重新给权限（保险操作）
chmod +x ~/.local/bin/wechat-start.sh

添加
sudo nano ~/桌面/wechat.desktop

[Desktop Entry]
Version=1.0
Name=微信
Comment=微信客户端
Exec=/home/pokes/.local/bin/wechat-start.sh
Icon=wechat
Terminal=false
Type=Application
Categories=Network;InstantMessaging;
StartupWMClass=WeChat
```



## 第二节：远程桌面XFCE里Chrome沙箱权限不足

先将Chrome浏览器用鼠标拖到桌面

```bash
mkdir -p ~/.local/share/applications
mousepad ~/.local/share/applications/google-chrome.desktop
```

sudo nano google-chrome.desktop

```bash
# 打开sudo nano google-chrome.desktop替换所有内容
[Desktop Entry]
Name=Google Chrome
Exec=/usr/bin/google-chrome-stable --no-sandbox %U
Terminal=false
Type=Application
Icon=google-chrome
StartupWMClass=Google-chrome
Categories=Network;WebBrowser;

# 或者
cat > ~/桌面/wechat.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Name=微信
Comment=微信客户端
# 这里的Exec=后面，根据你上面which的结果修改
Exec=bash -c "pgrep -x wechat && wmctrl -xa 'WeChat' || wechat --minimize-to-tray"
Icon=wechat
Terminal=false
Type=Application
Categories=Network;InstantMessaging;
StartupWMClass=WeChat
EOF

```

之后在 XFCE 菜单里找到 Chrome，就能直接点开用了。
