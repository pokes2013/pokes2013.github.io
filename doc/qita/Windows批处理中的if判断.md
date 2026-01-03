

# Windows批处理中的if判断



if 命令是批处理程序中条件判断的命令，根据得出的判断结果，执行相对应的操作。
if 命令基本有以下几种用法 。

## 1、判断指定的文件名是否存在

IF [NOT] EXIST filename command

```
@echo off
if not exist ./test.bat echo test.bat is not exist!
if exist ./temp.bat call temp.bat
pause
```

执行结果：

```
test.bat is not exist!
这是一个临时的测试批处理
请按任意键继续. . .
```

## 2、判断数值或者字符串相等

IF [/I] string1 compare-op string2 command
/I 开关 (如果指定) 说明要进行的字符串比较不分大小写
其中， compare-op 可以是:

```
EQU - 等于
NEQ - 不等于
LSS - 小于
LEQ - 小于或等于
GTR - 大于
GEQ - 大于或等于
```



```
@echo off

set "str1=this ia a test!"

set "str2=hello world!"

set num=100

if "%str1%"=="%str2%" (echo str1 等于 str2) else echo str1 不等于str2

if "%str2%" equ "Hello World!" (echo %str2% ) else (echo str2 不等于 Hello World)

if /i "%str2%" equ "Hello World!" (echo %str2% ) else (echo str2 不等于 Hello World)

if %num% equ 100 (echo num 等于 100) else echo num 不等于 100


pause
```

执行结果：

```
str1 不等于str2
str2 不等于 Hello World
hello world!
num 等于 100
请按任意键继续. . .
```

## 3、结合 ERRORLEVEL 使用

if errorlevel value command 含义：如果返回的错误码值大于或等于 value 时，将执行 cmmand

```
@echo off

:START
choice /c YNC /m "确认请选Y，否请按N，取消按C." /T 3 /D C
if errorlevel 3 goto CANCEL
if errorlevel 2 goto NO
if errorlevel 1 goto YES

:YES
echo 你的选择是YES!
goto END

:NO
echo 你的选择是NO!
goto END

:CANCEL
echo 你的选择是CANCEL!

:END
goto START

pause
```

执行结果：

```
确认请选Y，否请按N，取消按C. [Y,N,C]?Y
你的选择是YES!
确认请选Y，否请按N，取消按C. [Y,N,C]?N
你的选择是NO!
确认请选Y，否请按N，取消按C. [Y,N,C]?C
你的选择是CANCEL!
确认请选Y，否请按N，取消按C. [Y,N,C]?
```

## 4、判官变量是否已经被定义

```
@echo off

set "str=this ia a test!"

set num=100

if defined str echo str 已经被定义了

if defined num echo num 已经被定义了

if not defined var echo var 没有被定义

pause
```

执行结果：

```
str 已经被定义了
num 已经被定义了
var 没有被定义
请按任意键继续. . .
```

## 5、else 使用的注意事项

```
ELSE 子句必须出现在同一行上的 IF 之后。例如:

    IF EXIST filename. (
        del filename.
    ) ELSE (
        echo filename. missing.
    )
由于 del 命令需要用新的一行终止，因此以下子句不会有效:

IF EXIST filename. del filename. ELSE echo filename. missing

由于 ELSE 命令必须与 IF 命令的尾端在同一行上，以下子句也
不会有效:

    IF EXIST filename. del filename.
    ELSE echo filename. missing

如果都放在同一行上，以下子句有效:

    IF EXIST filename. (del filename.) ELSE echo filename. missing
```

