import os
from pathlib import Path

# ==================== 只需要改这1行！====================
# 把下面的路径改成你文件实际所在的目录（复制粘贴文件所在文件夹的路径）
TARGET_DIR = r"E:\DATA\GitData\pokes\pokes2025\doc\huawei"
# ========================================================

SAVE_FILENAME = "md_files_list.md"  # 保存结果的文件名（不用改）
EXCLUDE_FILE = "list.md"  # 要过滤的文件（不用改）

def find_md_files():
    """直接搜索指定绝对目录，不递归，显示所有文件供排查"""
    target_path = Path(TARGET_DIR)
    print(f"📂 正在搜索绝对目录（不递归）：{target_path}")
    
    # 检查目录是否存在
    if not target_path.exists():
        print(f"❌ 错误：目录不存在！请检查 TARGET_DIR 配置是否正确")
        return []
    
    # 打印目录下所有文件（帮你确认脚本能看到哪些文件）
    all_files = list(target_path.iterdir())
    print(f"\n📋 该目录下所有文件（共{len(all_files)}个）：")
    for idx, file in enumerate(all_files, 1):
        file_type = "📄 文件" if file.is_file() else "📁 文件夹"
        print(f"  {idx}. {file_type}：{file.name}（后缀：{file.suffix}）")
    
    # 筛选符合条件的.md文件（排除list.md）
    md_files = []
    for file in all_files:
        if (file.is_file()  # 是文件
            and file.suffix.lower() == ".md"  # 后缀是.md（大小写兼容）
            and file.name.lower() != EXCLUDE_FILE.lower()):  # 排除list.md
            md_files.append(file)
    
    return md_files

def generate_links(md_files):
    """生成你要的 Markdown 链接格式"""
    links = []
    # 以脚本运行目录为基准，生成相对路径（符合你的需求）
    base_dir = Path.cwd()
    print(f"\n📌 脚本运行目录（生成相对路径的基准）：{base_dir}")
    
    for file in md_files:
        file_title = file.stem  # 去掉.md后缀
        relative_path = file.relative_to(base_dir).as_posix()  # 相对路径（/分隔符）
        link = f"- [{file_title}]({relative_path})"
        links.append(link)
        print(f"🔗 生成链接：{link}")
    
    return links

def save_links(links):
    """自动保存结果"""
    save_path = Path(SAVE_FILENAME).absolute()
    with open(save_path, "w", encoding="utf-8") as f:
        f.write("\n".join(links))
    print(f"\n💾 结果已保存到：{save_path}")

if __name__ == "__main__":
    print("="*60)
    print("          Markdown链接生成工具（绝对路径版）")
    print("="*60)
    
    # 1. 找文件（显示所有文件供排查）
    md_files = find_md_files()
    
    if not md_files:
        print(f"\n❌ 未找到符合条件的.md文件（已排除{EXCLUDE_FILE}）")
    else:
        print(f"\n✅ 共找到 {len(md_files)} 个符合条件的.md文件")
        # 2. 生成链接
        links = generate_links(md_files)
        # 3. 保存
        save_links(links)
    
    print("\n" + "="*60)