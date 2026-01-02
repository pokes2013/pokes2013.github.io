## 1、字符串内置方法~大小写


```python
message = 'zhaorui iS a beautiful girl!'

# capitalize将字符串得第一个字符转换成大写

msg = message.capitalize()   #将字符串得第一个字符转换成大写
print(msg)

# title每个单词得首字母大写
msg = message.title()      #每个单词得首字母大写
print(msg)

# istitle判断

cmd = msg.istitle()           #判断每个单词得首字母是否大写
print(cmd)

spokes = message.istitle()    #判断每个单词得首字母是否大写
print(spokes)

# upper 全部转换成大写

msg = message.upper()
print(msg)

# lower 全部转换成小写
msg = message.lower()
print(msg)


len计算字符串长度

print(len(msg))          
```

    Zhaorui is a beautiful girl!
    Zhaorui Is A Beautiful Girl!
    True
    False
    ZHAORUI IS A BEAUTIFUL GIRL!
    zhaorui is a beautiful girl!
    28


## 2、字符串替换replace


```python
语法：变量.replace(“被替换的内容”，“替换后的内容”[，次数])
```


```python
#删除符号
str1 = "212、Python用replace()函数删除制定  符号"
str2 = str1.replace('、', '')
str3 = str2.replace(' ', '')
print(str3)
```

    212Python用replace()函数删除制定符号



```python
# # 内容比较
s1='abc'
s2="abc"

print(s1 == s2)
print(s1 is s2)
```

    True
    True


## 3、字符串截取


```python
# 字符串截取
#Python 提供了很多截取字符串的方法，被称为“切片（slicing）”。字符串分割

#语法：string[end: step]
#start 头下标,开始,，以0开头
#end 尾下标,结尾
#step 步长



filename = 'picture.png'
# 类似range
print(filename[0:4])
# 省略
print(filename[7:])
# 负数
print(filename[-4:])


name = 'pokes'
print(name[::-1])  # -1表示倒序
```

    pict
    .png
    .png
    sekop


实例


```python
str = "abc-123-如果我是DJ你会爱我吗.mp4"
str = str[0:7]           #默认步长是1，可以不写
print(str)
```

    abc-123



```python
str = "abc-123-如果我是DJ你会爱我吗.mp4"
str = str[0:-9]           #负数是从右往左截取
print(str)
```

    abc-123-如果我是DJ



```python
str = "abc-123-如果我是DJ你会爱我吗.mp4"
str = str[8:]           #不写右边就是一直到结尾
print(str)
```

    如果我是DJ你会爱我吗.mp4



```python
#分割符号截取 关键字split，有时候也叫列截取
#语法格式：变量.split('分隔符',次数)
str = "abc-123-如果我是DJ你会爱我吗.mp4"
str = str.split('-')          #次数不写，则默认为最大次数
print(str)
```

    ['abc', '123', '如果我是DJ你会爱我吗.mp4']


## 4、字符串查找find

find方法检测字符串中是否包含子字符串str ，如果指定 beg（开始） 和 end（结束） 范围，则检查是否包含在指定范围内，如果指定范围内如果包含指定索引值，如果不包含索引值，返回-1。返回的是需要查找的字符串的下标
#变量.find(“要查找的内容”，[开始位置，结束位置])


```python
str = "abc-123-如果我是DJ你会爱我吗.mp4"
str = str.find('DJ')
print(str)                    ##返回的是需要查找的字符串的下标,不包含则返回-1
```

    12


## 5、字符串处理-高级用法.py


```python
# 详情参考：https://blog.csdn.net/csdn15698845876/article/details/73469234

s = "   %pokes$@163&.com*   "

ss = s.strip().strip("%").lstrip('$').rstrip().rstrip('*')
print(ss)

```

    pokes$@163&.com

### 连续替换多个字符串



```python
#替换多个字符串.py

def zifu(str, x, y, z):
    strin = str.replace(x, '').replace(y, '').replace(z, '')
    print(strin)


zifu("pokes，@163.com,kkkkk", "，", ",", "163")
```

    pokes@.comkkkkk

### 检测包含

```python
#检测包含

def baohan(str, bh01, bh02, bh03, bh04):

    if (bh01 in str) == True:
        print("包含了：" + bh01)

    if (bh02 in str) == True:
        print("包含了：" + bh02)
    else:
        print("不包含了：" + bh02)

    if (bh03 in str) == True:
        print("包含了：" + bh03)

    if (bh04 in str) == True:
        print("包含了：" + bh04)

baohan("[韩国][我朋友的老姐].2016.Uncut.720p.HDRip.H264-ob.mp4", "韩国", "老姐", "朋友", "2016")
```

    包含了：韩国
    包含了：老姐
    包含了：朋友
    包含了：2016

### 判断字符串是数字还是字母

```python
#判断字符串是数字还是字母

# isdigit函数判断

str_1 = "123"
str_2 = "Abc"
str_3 = "123Abc"

print(str_1.isdigit())
print(str_2.isdigit())
print(str_3.isdigit())


from txdpy import is_num, is_chinese, is_letter, is_Bletter, is_Sletter, is_num_letter

s1 = 's1'
s2 = 'ss'
s3 = 's三'
s4 = 'SSSS'
s5 = '测试'
s6 = '6666'
s7 = '测试777'

# 是否为纯数字
print(is_num(s6))
print(is_num(s7))
# 是否为纯汉字
print(is_chinese(s5))
print(is_chinese(s7))
# 是否为纯字母
print(is_letter(s1))
print(is_letter(s2))
# 是否为纯大写字母
print(is_Bletter(s4))
print(is_Bletter(s2))
# 是否为纯小写字母
print(is_Sletter(s4))
print(is_Sletter(s2))
# 是否为只包含 字母 或 数字 或 数字和字母
print(is_num_letter(s1))
print(is_num_letter(s4))
```

### 正则表达式

- 数字：\u0030-\u0039
- 汉字：\u4e00-\u9fa5
- 大写字母：\u0041-\u005a
- 小写字母：\u0061-\u007a
- 英文字母：\u0041-\u007a

注：更多的编码范围可参考另博主的整理：https://blog.csdn.net/weixin_34206263/article/details/112031865


```python
# 只保留汉字
import re

str1 = " 12312313Python用replace()函数删除制定  符号  "
str2 = re.sub('([^\u4e00-\u9fa5])', '', str1)
print(str2)              # "用函数删除制定符号"


# 只保留字符串中的汉字和数字

str3 = re.sub('([^\u4e00-\u9fa5\u0030-\u0039])', '', str1)
print(str3)     # "212用函数删除制定符号"
```

    用函数删除制定符号
    12312313用函数删除制定符号

