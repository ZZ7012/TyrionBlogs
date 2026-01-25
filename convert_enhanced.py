#!/usr/bin/env python3
import os
import re
import sys
import shutil
from urllib.parse import quote

#-------------手动设置图片路径-------------------------
# 📁 图片集中目录（根据你的设置）
ATTACH_DIR = "resources"
#---------------------------------------------------

# 支持的图片扩展名
IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'tiff']
IMG_EXTS_PATTERN = '|'.join(IMG_EXTS)

# 匹配 ![[图片名.xxx]] 的 Obsidian 图片 wiki 链接
wiki_img_pattern = re.compile(r'!\[\[([^\[\]]+?\.(?:' + IMG_EXTS_PATTERN + r'))\]\]')

# 匹配已有的 Markdown 图片引用 ![](resources/xxx.png) 并检查是否有未编码的空格
markdown_img_pattern = re.compile(r'!\[\]\(([^)]*?\.(?:' + IMG_EXTS_PATTERN + r'))\)')

# 记录图片重命名映射
rename_map = {}

def rename_images(vault_root):
    """重命名含空格图片文件为中划线版本"""
    attach_dir_abs = os.path.join(vault_root, ATTACH_DIR)
    print(f"📁 扫描图片目录：{attach_dir_abs}")
    if not os.path.isdir(attach_dir_abs):
        print(f"❌ 错误：图片目录不存在：{attach_dir_abs}")
        return

    for filename in os.listdir(attach_dir_abs):
        if ' ' in filename and any(filename.lower().endswith(ext) for ext in IMG_EXTS):
            new_filename = filename.replace(' ', '-')
            src = os.path.join(attach_dir_abs, filename)
            dst = os.path.join(attach_dir_abs, new_filename)

            # 避免重名
            count = 1
            while os.path.exists(dst):
                name, ext = os.path.splitext(new_filename)
                dst = os.path.join(attach_dir_abs, f"{name}-{count}{ext}")
                count += 1

            os.rename(src, dst)
            rename_map[filename] = os.path.basename(dst)
            print(f"📝 重命名: {filename} → {os.path.basename(dst)}")
        else:
            rename_map[filename] = filename

def fix_markdown_img_references(content):
    """修复已有 Markdown 格式中的未编码空格"""
    def replacer(match):
        img_path = match.group(1)
        # 检查是否包含未编码的空格
        if ' ' in img_path:
            # 对路径进行 URL 编码
            img_path_encoded = quote(img_path, safe='/')
            print(f"🔹 修复空格编码: ![]('{img_path}') → ![]({img_path_encoded})")
            return f"![]({img_path_encoded})"
        return match.group(0)
    
    return markdown_img_pattern.sub(replacer, content)

def process_file(file_path, vault_root, dry_run=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    has_wiki_links = wiki_img_pattern.search(content)
    has_unencoded_spaces = markdown_img_pattern.search(content) and ' ' in content

    if not has_wiki_links and not has_unencoded_spaces:
        print(f"ℹ️ 无需处理，跳过: {file_path}")
        return

    print(f"✅ 处理文件: {file_path}")

    # 第一步：转换 Obsidian 格式
    if has_wiki_links:
        def wiki_replacer(match):
            original_image_name = match.group(1)
            new_image_name = rename_map.get(original_image_name, original_image_name)
            final_path = os.path.join(ATTACH_DIR, new_image_name).replace("\\", "/")
            final_path_encoded = quote(final_path, safe='/')
            print(f"🔹 转换: {match.group(0)} → ![]({final_path_encoded})")
            return f"![]({final_path_encoded})"

        content = wiki_img_pattern.sub(wiki_replacer, content)

    # 第二步：修复 Markdown 格式中的空格编码
    if has_unencoded_spaces:
        content = fix_markdown_img_references(content)

    if dry_run:
        print(f"👀 预览模式，未写入文件: {file_path}")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 写入完成: {file_path}")

def process_directory(root_dir, dry_run=True):
    rename_images(root_dir)
    print("\n" + "="*60)
    print("开始处理 Markdown 文件中的图片引用...")
    print("="*60 + "\n")

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path, root_dir, dry_run=dry_run)

if __name__ == "__main__":
    vault_root = os.getcwd()
    print(f"🔎 开始处理 Vault 目录: {vault_root}")
    print("="*60)
    process_directory(vault_root, dry_run=False)
    print("\n✅ 所有处理完成！")
