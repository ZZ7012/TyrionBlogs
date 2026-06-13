#!/usr/bin/env python3
"""Fix image filenames with spaces — rename files and update all markdown references."""
import os
import re

POSTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "posts")
IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'tiff']

def find_images_with_spaces(root):
    """Walk the tree, find image files with spaces in the name."""
    to_rename = []  # (full_path, new_name)
    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            ext = fn.rsplit('.', 1)[-1].lower()
            if ext in IMG_EXTS and ' ' in fn:
                new_fn = fn.replace(' ', '-')
                to_rename.append((os.path.join(dirpath, fn), new_fn))
    return to_rename

def rename_files(to_rename):
    """Rename files on disk, return {old_basename: new_basename} map."""
    name_map = {}
    for full_path, new_name in to_rename:
        dirname = os.path.dirname(full_path)
        new_full = os.path.join(dirname, new_name)
        # Handle collisions
        counter = 1
        base, ext = os.path.splitext(new_name)
        while os.path.exists(new_full):
            new_full = os.path.join(dirname, f"{base}-{counter}{ext}")
            new_name = os.path.basename(new_full)
            counter += 1
        old_name = os.path.basename(full_path)
        os.rename(full_path, new_full)
        name_map[old_name] = new_name
        print(f"  {old_name}  →  {new_name}")
    return name_map

def update_markdown_refs(root, name_map):
    """Update all .md files that reference renamed images."""
    pattern = re.compile(r'\]\((\.?/?resources/)(Pasted\s+image\s+[^)]+\.(?:' + '|'.join(IMG_EXTS) + r'))\)')
    updated_count = 0

    for dirpath, _, filenames in os.walk(root):
        for fn in filenames:
            if not fn.endswith('.md'):
                continue
            fpath = os.path.join(dirpath, fn)
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()

            new_content = content

            def replacer(m):
                nonlocal updated_count
                prefix, img_name = m.group(1), m.group(2)
                if img_name in name_map:
                    updated_count += 1
                    print(f"  {fn}: {img_name} → {name_map[img_name]}")
                    return f"]({prefix}{name_map[img_name]})"
                # Also handle any space → hyphen (URL encoding fallback)
                if ' ' in img_name:
                    # If not in name_map, do a direct replacement
                    new_img = img_name.replace(' ', '-')
                    updated_count += 1
                    print(f"  {fn}: {img_name} → {new_img}")
                    return f"]({prefix}{new_img})"
                return m.group(0)

            new_content = pattern.sub(replacer, content)

            if new_content != content:
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

    return updated_count

def main():
    print("=== Step 1: Find images with spaces ===\n")
    to_rename = find_images_with_spaces(POSTS_DIR)

    if not to_rename:
        print("No images with spaces found - nothing to do!")
        return

    print(f"Found {len(to_rename)} images to rename:\n")

    print("=== Step 2: Rename image files ===\n")
    name_map = rename_files(to_rename)

    print(f"\n=== Step 3: Update markdown references ===\n")
    updated = update_markdown_refs(POSTS_DIR, name_map)

    print(f"\nDone! Renamed {len(name_map)} files, updated {updated} references.")

if __name__ == "__main__":
    main()
