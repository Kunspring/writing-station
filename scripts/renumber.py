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
    # 获取所有文章ID，按名称排序
    doc_ids = []
    for f in os.listdir(DOCS_DIR):
        if f.endswith(".txt"):
            doc_ids.append(f.replace(".txt", ""))
    doc_ids.sort()

    # 重新编号：从1开始依次分配
    for idx, doc_id in enumerate(doc_ids, start=1):
        meta = load_meta(doc_id)
        meta["number"] = idx
        save_meta(doc_id, meta)
        print(f"{doc_id} → #{idx}")

    # 更新计数器为下一个可用编号
    next_num = len(doc_ids) + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(next_num))
    print(f"计数器已设为 {next_num}")

if __name__ == "__main__":
    main()
