"""为所有缺失缩略图的封面生成 WebP 缩略图"""
import os, json, sys
from PIL import Image

DOCS_DIR = "docs"
COVERS_DIR = "static/covers"
MAX_SIZE = 300  # 缩略图最大边长

def make_thumb(image_path, thumb_path):
    try:
        img = Image.open(image_path)
        img.thumbnail((MAX_SIZE, MAX_SIZE))
        img.save(thumb_path, "WEBP", quality=80)
        return True
    except Exception as e:
        print(f"  FAIL: {image_path} -> {e}")
        return False

# 收集缺失缩略图的封面
missing = []
for f in sorted(os.listdir(DOCS_DIR)):
    if not f.endswith(".meta.json"):
        continue
    path = os.path.join(DOCS_DIR, f)
    meta = json.load(open(path))
    cover = meta.get("cover", "")
    if not cover:
        continue
    # cover 路径格式: /static/covers/27_ee8e4b25.png
    basename = os.path.basename(cover)
    name_no_ext = os.path.splitext(basename)[0]
    thumb_filename = f"{name_no_ext}_thumb.webp"
    thumb_path = os.path.join(COVERS_DIR, thumb_filename)
    cover_abs = os.path.join(COVERS_DIR, basename)

    if os.path.exists(thumb_path):
        # 已有缩略图但 meta 未记录
        if not meta.get("cover_thumb"):
            meta["cover_thumb"] = f"/static/covers/{thumb_filename}"
            json.dump(meta, open(path, "w"), ensure_ascii=False, indent=2)
            print(f"  UPDATED meta: {f} -> cover_thumb")
        continue

    if not os.path.exists(cover_abs):
        print(f"  MISSING source: {cover_abs}")
        continue

    missing.append((f, cover_abs, thumb_path, thumb_filename))

print(f"Missing thumbnails: {len(missing)}")

for f, src, dst, thumb_fn in missing:
    print(f"  Generating: {thumb_fn} (from {os.path.basename(src)}) ...")
    if make_thumb(src, dst):
        doc_path = os.path.join(DOCS_DIR, f)
        meta = json.load(open(doc_path))
        meta["cover_thumb"] = f"/static/covers/{thumb_fn}"
        json.dump(meta, open(doc_path, "w"), ensure_ascii=False, indent=2)
        sz = os.path.getsize(dst)
        print(f"    OK ({sz/1024:.0f}KB)")

print("Done!")
