# ENSP和HCI共存方法



## 一、安装virtualBox

版本： 5.2.44

## 二、安装ENSP模拟器

## 三、打开注册表

定位到“计算机\HKEY_LOCAL_MACHINE\SOFTWARE\Oracle\VirtualBox”

## 四、修改注册表

手动修改右侧Version和VersionExt版本为6.0.14

## 五、安装HCL

版本： 安装与VirtualBox6.0.14兼容的（比如：5.0等）

## 六、将注册表中修改的改回原来的内容

注意： 如果不改回5.2.44，则ensp不能运行

原理：中间改注册表为了欺骗hcl，virtualbox6.0.14已经安装了
注意：步骤不要改，最后可能会出现ensp改文字大小等一些小问题，但是只是提示一下，不影响使用。





H3C课程，老师讲得不错！

https://www.bilibili.com/video/BV1Su4y1G7ni?spm_id_from=333.788.player.switch&vd_source=9dc23d072b0edbf78ffed52f1fcb2318&p=9
