import os

# 1. 定义java变量（可按需修改，满足变量化要求）
java_var = "html+css"

# 2. 定义需要排除的文件列表
exclude_files = ["_sidebar.md", "README.md"]

# 3. 存储生成的侧边栏条目
sidebar_items = []

# 4. 遍历当前目录下的所有文件
for file_name in os.listdir("."):
    # 筛选条件：.md结尾 + 不在排除列表中
    if file_name.endswith(".md") and file_name not in exclude_files:
        # 去除.md后缀，作为侧边栏显示文本和路径一部分
        file_title = os.path.splitext(file_name)[0]
        # 5. 拼接指定格式的侧边栏条目（包含文件名的完整路径）
        sidebar_item = f"* [{file_title}](doc/{java_var}/{file_title})"
        sidebar_items.append(sidebar_item)

# 6. 输出结果（两种方式：打印到控制台 + 可选写入_sidebar.md）
if __name__ == "__main__":
    # 打印所有侧边栏条目
    print("生成的侧边栏内容：")
    print("-" * 20)
    for item in sidebar_items:
        print(item)
    
    # 可选：将结果写入_sidebar.md文件（覆盖原有内容，如需追加可修改mode="a"）
    with open("_sidebar.md", "w", encoding="utf-8") as f:
        # 写入所有侧边栏条目，每行一个
        f.write("\n".join(sidebar_items))
    
    print("-" * 20)
    print(f"成功生成 {len(sidebar_items)} 个侧边栏条目，已写入 _sidebar.md 文件")