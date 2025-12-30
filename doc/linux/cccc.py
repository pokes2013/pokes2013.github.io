import glob
import os

def generate_md_links():
    # 1. 核心可配置变量
    target_dir = "linux"  # linux目录提取为变量，可灵活修改
    output_file = "md_links.txt"  # 输出文件名
    # 定义需要排除的文件名称（无需带.md后缀，兼容精准匹配）
    exclude_files = ["_sidebar", "README"]

    # 2. 获取当前目录下所有.md后缀文件（不递归子目录）
    md_files = glob.glob("*.md")
    if not md_files:
        print("提示：当前目录下未找到任何.md后缀文件！")
        return

    # 3. 遍历构造指定格式的Markdown链接，同时排除目标文件
    link_list = []
    for md_file in md_files:
        # 安全去除.md后缀（兼容文件名含多个"."的场景）
        file_name_without_suffix = os.path.splitext(md_file)[0]
        
        # 排除判断：如果无后缀文件名在排除列表中，跳过当前文件
        if file_name_without_suffix in exclude_files:
            continue  # 跳过排除文件，不生成链接
        
        # 构造链接：前缀添加"- "，拼接target_dir变量
        markdown_link = f"- [{file_name_without_suffix}](./doc/{target_dir}/{file_name_without_suffix})"
        link_list.append(markdown_link)

    # 4. 输出结果（终端打印 + 保存到文件）
    # 方式1：终端逐行打印所有有效链接
    print(f"原始找到 {len(md_files)} 个.md文件，排除 {len(exclude_files)} 个文件后，生成 {len(link_list)} 个有效链接：")
    print("-" * 50)
    for link in link_list:
        print(link)
    print("-" * 50)

    # 方式2：保存到文件（utf-8编码避免中文乱码，异常捕获）
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(link_list))
        print(f"所有有效链接已保存到 {output_file} 文件中！")
    except Exception as e:
        print(f"保存文件失败，异常信息：{e}")

if __name__ == "__main__":
    generate_md_links()