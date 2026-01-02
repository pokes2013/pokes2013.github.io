import webbrowser

# print("注意：如果关键字中有空格，请讲空格替换成加号")
str01 = input("请输入你得搜索关键字：")


# str01 = "唐朝诡事录"
str02 = "https://www.baidu.com/baidu?tn=baidu&word="

str03 = str02 + str01

webbrowser.open(str03)
