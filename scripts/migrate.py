import os, json, shutil

DOCS_DIR = "docs"
COMMENTS_DIR = "comments"
# 遍历所有 .txt 文件
for filename in os.listdir(DOCS_DIR):
    if filename.endswith(".txt") and not filename.startswith("."):
        old_id = filename.replace(".txt", "")
        meta_path = os.path.join(DOCS_DIR, f"{old_id}.meta.json")
        if not os.path.exists(meta_path):
            continue
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        number = meta.get("number")
        if number is None:
            continue
        new_id = str(number)
        if old_id != new_id:
            # 重命名文件
            os.rename(
                os.path.join(DOCS_DIR, f"{old_id}.txt"),
                os.path.join(DOCS_DIR, f"{new_id}.txt")
            )
            os.rename(meta_path, os.path.join(DOCS_DIR, f"{new_id}.meta.json"))
            # 迁移评论文件（如果存在）
            old_comments = os.path.join(COMMENTS_DIR, f"{old_id}.comments.json")
            new_comments = os.path.join(COMMENTS_DIR, f"{new_id}.comments.json")
            if os.path.exists(old_comments):
                os.rename(old_comments, new_comments)
            print(f"迁移: {old_id} -> {new_id}")