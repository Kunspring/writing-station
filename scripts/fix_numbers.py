import json
import os

DOCS_DIR = "docs"
COUNTER_FILE = os.path.join(DOCS_DIR, ".counter.txt")

def load_meta(doc_id):
    path = os.path.join(DOCS_DIR, f"{doc_id}.meta.json")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_meta(doc_id, meta):
    path = os.path.join(DOCS_DIR, f"{doc_id}.meta.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def main():
    # 获取所有文章ID
    doc_ids = []
    for f in os.listdir(DOCS_DIR):
        if f.endswith(".txt"):
            doc_ids.append(f.replace(".txt", ""))
    
    # 按文件名排序（保证可重复）
    doc_ids.sort()
    
    # 分配编号从1开始
    next_num = 1
    for doc_id in doc_ids:
        meta = load_meta(doc_id)
        if "number" not in meta:
            meta["number"] = next_num
            save_meta(doc_id, meta)
            print(f"为 {doc_id} 分配编号 {next_num}")
        else:
            print(f"{doc_id} 已有编号 {meta['number']}，跳过")
        next_num += 1
    
    # 更新计数器文件为下一个可用编号
    with open(COUNTER_FILE, "w") as f:
        f.write(str(next_num))
    print(f"计数器已更新为 {next_num}")

if __name__ == "__main__":
    main()
