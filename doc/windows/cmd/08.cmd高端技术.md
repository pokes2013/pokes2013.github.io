# cmd高端技术

测试文件

## 算数运算

加+，减-，乘*，除/，取余%

基本用法：

```
C:\Users\Anita>set /a 1+2
3
C:\Users\Anita>set /a 2*2
4
C:\Users\Anita>set /a 10/5
2
C:\Users\Anita>set /a 10/3    #除法只显示整数
3
C:\Users\Anita>set /a 10%3    #取余数
1
C:\Users\Anita>
```

脚本实例：

```
@echo off

set /a var = 1 + 2
echo %var%

pause

关于计算的优先级和我们数学里面是一样的加括号，先算括号内的。
@echo off

set /a var = 10*(9+ 2)
echo %var%

pause
```

## 管道符的使用

```
E:\>dir | find ".flv"
2021-12-11  18:13        58,636,098 四种方法教你快速去除视频水印.flv

E:\>dir | find ".txt"
2020-02-29  15:53               101 Everything本机远程搜索配置文件.txt



帅选建立连接的IP和端口
C:\Users\Anita>netstat -an | find "ESTABLISHED"
  TCP    10.10.30.100:1030      121.41.165.217:443     ESTABLISHED
  TCP    10.10.30.100:1212      52.139.250.253:443     ESTABLISHED
  TCP    10.10.30.100:1890      58.211.107.14:6667     ESTABLISHED
  TCP    127.0.0.1:2093         127.0.0.1:25340        ESTABLISHED
  TCP    127.0.0.1:25340        127.0.0.1:2093         ESTABLISHED
  TCP    192.168.80.13:2099     10.5.6.51:22           ESTABLISHED
  TCP    192.168.80.13:2110     222.188.43.129:443     ESTABLISHED
  TCP    192.168.80.13:2172     40.119.211.203:443     ESTABLISHED
  TCP    192.168.80.13:2442     10.5.6.51:22           ESTABLISHED
  TCP    192.168.80.13:3145     110.43.213.99:443      ESTABLISHED
  TCP    192.168.80.13:3460     108.177.125.188:5228   ESTABLISHED
  TCP    192.168.80.13:3520     52.139.250.209:443     ESTABLISHED
  TCP    192.168.80.13:3539     34.237.73.95:443       ESTABLISHED
  TCP    192.168.80.13:4306     121.4.25.190:443       ESTABLISHED
  TCP    192.168.80.13:4307     120.92.208.233:7826    ESTABLISHED
  TCP    192.168.80.13:4378     180.163.151.34:443     ESTABLISHED
  TCP    192.168.80.13:4449     61.155.136.166:443     ESTABLISHED
```

```
@echo off

set name=type C:\Temp\muluming.txt


for /f %%i in (C:\Temp\muluming.txt) do md D:\00suoying2022\归档-%%i


for /f %%i in (C:\Temp\wenjian02.txt) do echo nul>D:\00suoying2022\%%i.mp4


提取当前目录名

for %%i in ("%cd%") do echo %%~ni>C:\Temp\muluming.txt

将命令执行的结果赋值给变量

for /F %%i in ('git rev-parse --short HEAD') do ( set commitid=%%i)
echo commitid=%commitid%


pause
```
