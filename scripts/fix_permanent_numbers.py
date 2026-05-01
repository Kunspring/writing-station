import json
import os

DOCS_DIR = "docs"
COUNTER_FILE = os.path.join(DOCS_DIR, ".counter.txt")

def load_meta(doc_id):
    path = os.path.join(DOCS_DIR, f"{doc_id}.meta.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"authors": []}

def save_meta(doc_id, meta):
    path = os.path.join(DOCS_DIR, f"{doc_id}.meta.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def main():
    # 获取所有文章，按文件名排序（可改成按创建时间排序，但文件系统不易获取，用文件名保证一致性）
    doc_ids = []
    for f in os.listdir(DOCS_DIR):
        if f.endswith(".txt"):
            doc_ids.append(f.replace(".txt", ""))
    doc_ids.sort()

    # 找出当前已有的最大编号，若没有则从 1 开始
    existing_numbers = []
    for doc_id in doc_ids:
        meta = load_meta(doc_id)
        if "number" in meta:
            existing_numbers.append(meta["number"])
    if existing_numbers:
        next_num = max(existing_numbers) + 1
    else:
        next_num = 1

    # 为每篇文章分配唯一编号：若已有编号且未重复，保留；否则赋予新编号
    used_numbers = set()
    for doc_id in doc_ids:
        meta = load_meta(doc_id)
        current_num = meta.get("number")
        if current_num is not None and current_num not in used_numbers:
            # 保留原有编号，但确保不重复
            used_numbers.add(current_num)
        else:
            # 分配新编号
            meta["number"] = next_num
            used_numbers.add(next_num)
            next_num += 1
        save_meta(doc_id, meta)
        print(f"{doc_id} → 编号 #{meta['number']}")

    # 更新计数器为下一个可用编号（最大编号+1）
    max_used = max(used_numbers) if used_numbers else 0
    new_counter = max_used + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(new_counter))
    print(f"计数器已更新为 {new_counter}（新文章将从 #{new_counter} 开始）")

if __name__ == "__main__":
    main()
