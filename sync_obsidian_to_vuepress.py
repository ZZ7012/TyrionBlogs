#!/usr/bin/env python3
"""
将 Obsidian 笔记同步转换为 VuePress 博客格式。

处理内容：
1. ![[image.png]] wiki 链接 → ![image](./resources/image.png) Markdown 链接
2. 图片文件名空格 → 短横线
3. 自动补 ---\ntitle: 文件名\n--- frontmatter
4. 同步图片资源文件
"""

import os
import re
import shutil

# ============== 配置 ==============
OBSIDIAN_SRC = r"C:\Users\Rongz\Documents\00Note\LearningNotes\01Autosar"
BLOG_TARGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "posts", "Autosar")
# ==================================

IMG_EXTS = {"png", "jpg", "jpeg", "gif", "bmp", "svg", "webp", "tiff"}
IMG_EXT_PATTERN = "|".join(IMG_EXTS)

# 匹配 Obsidian wiki 图片链接: ![[filename.png]]
WIKI_IMG_RE = re.compile(
    r"!\[\[([^\[\]]+?\.(?:" + IMG_EXT_PATTERN + r"))\]\]", re.IGNORECASE
)

# 匹配已有的 Markdown 图片引用
MD_IMG_RE = re.compile(
    r"!\[.*?\]\(([^)]*?\.(?:" + IMG_EXT_PATTERN + r"))\)", re.IGNORECASE
)

stats = {"files_synced": 0, "images_copied": 0, "links_fixed": 0,
         "links_missing": 0, "errors": []}


def safe_filename(name):
    """把文件名中的空格替换为短横线，处理连续空格。"""
    return re.sub(r"\s+", "-", name.strip())


def extract_title(filepath):
    """从文件路径中提取标题：用文件名（不含扩展名）作为 title。"""
    base = os.path.splitext(os.path.basename(filepath))[0]
    return safe_filename(base) if base else "Untitled"


def sync_images(src_res_dir, tgt_res_dir):
    """
    将源 resources/ 目录中的图片复制到目标目录，
    重命名含空格的文件名（空格→短横线）。
    返回 {旧文件名: 新文件名} 的映射。
    """
    name_map = {}
    if not os.path.isdir(src_res_dir):
        return name_map

    os.makedirs(tgt_res_dir, exist_ok=True)

    for fname in os.listdir(src_res_dir):
        src_path = os.path.join(src_res_dir, fname)
        if not os.path.isfile(src_path):
            continue

        ext = fname.rsplit(".", 1)[-1].lower()
        if ext not in IMG_EXTS:
            # 非图片文件不处理
            continue

        if " " in fname:
            new_name = fname.replace(" ", "-")
        else:
            new_name = fname

        # 处理重名冲突：优先按内容判断是否同一文件
        base, ext_part = os.path.splitext(new_name)
        dst_path = os.path.join(tgt_res_dir, new_name)
        if os.path.exists(dst_path):
            # 同路径、同尺寸 → 同一文件，跳过
            if os.path.getsize(dst_path) == os.path.getsize(src_path):
                name_map[fname] = new_name
                if not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
                    stats["images_copied"] += 1
                continue
            # 尺寸不同 → 真正冲突，追加编号
            counter = 1
            while os.path.exists(dst_path):
                new_name = f"{base}-{counter}{ext_part}"
                dst_path = os.path.join(tgt_res_dir, new_name)
                counter += 1

        name_map[fname] = new_name
        shutil.copy2(src_path, dst_path)
        stats["images_copied"] += 1

    return name_map


def convert_content(content, name_map):
    """
    转换 markdown 内容：
    1. ![[img.png]] → ![](./resources/img.png)，对不存在的图片注释掉
    2. 已有 Markdown 图片链接中的空格 → 短横线
    返回转换后的内容。
    """
    def wiki_replacer(m):
        old_name = m.group(1)
        # 规范化名称（空格→短横线）
        new_name = old_name.replace(" ", "-")
        # 检查该图片是否存在于源目录的 resources 中
        known = name_map.get(old_name) or name_map.get(new_name)
        if known:
            stats["links_fixed"] += 1
            return f"![{known}](./resources/{known})"
        else:
            stats["links_missing"] += 1
            return f"> [!warning] 图片丢失: {old_name}"

    content = WIKI_IMG_RE.sub(wiki_replacer, content)

    # 修复已有 Markdown 链接中的空格
    def md_spaces_replacer(m):
        path = m.group(0)
        if " " in path:
            fixed = path.replace(" ", "-")
            stats["links_fixed"] += 1
            return fixed
        return path

    content = MD_IMG_RE.sub(md_spaces_replacer, content)

    return content


def add_frontmatter(content, title):
    """如果文件没有 frontmatter，则在顶部添加。"""
    stripped = content.lstrip("\n")
    if stripped.startswith("---"):
        # 检查是否是真 frontmatter（第一行 --- 且后面还有 ---）
        lines = stripped.split("\n")
        if len(lines) > 1:
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    # 有闭合的 ---，是 frontmatter，不重复添加
                    return content
        # 第一行 --- 但不是 frontmatter（水平分隔线），仍然添加
    elif stripped.startswith("title:"):
        # 已经有 frontmatter 内容但不是标准格式
        return content

    return f"---\ntitle: {title}\n---\n\n{content}"


def sync_markdown(src_path, tgt_path, name_map):
    """同步单个 markdown 文件。"""
    try:
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        stats["errors"].append(f"读取失败 {src_path}: {e}")
        return

    content = convert_content(content, name_map)
    title = extract_title(src_path)
    content = add_frontmatter(content, title)

    os.makedirs(os.path.dirname(tgt_path), exist_ok=True)
    try:
        with open(tgt_path, "w", encoding="utf-8") as f:
            f.write(content)
        stats["files_synced"] += 1
    except Exception as e:
        stats["errors"].append(f"写入失败 {tgt_path}: {e}")


def main():
    print("=" * 60)
    print("Obsidian => VuePress: Sync Script")
    print(f"Source:  {OBSIDIAN_SRC}")
    print(f"Target:  {BLOG_TARGET}")
    print("=" * 60)

    if not os.path.isdir(OBSIDIAN_SRC):
        print(f"\n[SKIP] Obsidian source not found: {OBSIDIAN_SRC}")
        print("       This is expected on CI. Sync must be run locally before commit.")
        return

    # ============ Phase 1: Sync image resources ============
    print("\n[Phase 1] Scanning and syncing image resources...")
    all_name_maps = {}

    for dirpath, dirnames, _ in os.walk(OBSIDIAN_SRC):
        if os.path.basename(dirpath) == ".obsidian":
            dirnames[:] = []  # skip .obsidian
            continue

        if "resources" in dirnames:
            src_res = os.path.join(dirpath, "resources")
            rel = os.path.relpath(dirpath, OBSIDIAN_SRC)
            tgt_rel = os.path.join(BLOG_TARGET, rel) if rel != "." else BLOG_TARGET
            tgt_res = os.path.join(tgt_rel, "resources")
            name_map = sync_images(src_res, tgt_res)
            all_name_maps.update(name_map)

    # ============ Phase 2: Convert Markdown files ============
    print("\n[Phase 2] Converting Markdown files...")

    for dirpath, dirnames, filenames in os.walk(OBSIDIAN_SRC):
        if os.path.basename(dirpath) == ".obsidian":
            dirnames[:] = []
            continue

        for fname in filenames:
            if not fname.endswith(".md"):
                continue

            src_path = os.path.join(dirpath, fname)
            rel = os.path.relpath(src_path, OBSIDIAN_SRC)
            tgt_path = os.path.join(BLOG_TARGET, rel)

            sync_markdown(src_path, tgt_path, all_name_maps)

    # ============ Report ============
    print("\n" + "=" * 60)
    print("Sync Complete!")
    print(f"  Markdown files: {stats['files_synced']}")
    print(f"  Images synced:  {stats['images_copied']}")
    print(f"  Links fixed:    {stats['links_fixed']}")
    if stats["errors"]:
        print(f"  Errors:         {len(stats['errors'])}")
        for err in stats["errors"]:
            print(f"    * {err}")
    print("=" * 60)


if __name__ == "__main__":
    main()
