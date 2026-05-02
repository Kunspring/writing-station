#!/usr/bin/env python3
"""每日连载脚本：发布《灰域漂航》一章"""
import os, sys, json, requests

BASE_URL = "http://localhost:5000"
USERNAME = "misaka_mikoto"
PASSWORD = "railgun10032"
NOVEL_DIR = "/root/simple-writer/novel"
PROGRESS_FILE = os.path.join(NOVEL_DIR, "progress.json")

def get_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE) as f:
            return json.load(f)
    return {"chapter": 0}

def save_progress(prog):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(prog, f, ensure_ascii=False, indent=2)

def login():
    r = requests.post(f"{BASE_URL}/api/login", json={"username": USERNAME, "password": PASSWORD})
    data = r.json()
    if data.get("status") != "ok":
        print(f"登录失败: {data}")
        sys.exit(1)
    token = data["token"]
    print("登录成功")
    return token

def auth_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

def create_doc(token):
    r = requests.post(f"{BASE_URL}/api/create_doc", headers=auth_headers(token))
    data = r.json()
    if data.get("status") != "ok":
        print(f"创建文章失败: {data}")
        sys.exit(1)
    print(f"创建文章 #{data['doc_id']}")
    return data["doc_id"]

def set_title(token, doc_id, title):
    r = requests.post(f"{BASE_URL}/api/doc/{doc_id}/title", headers=auth_headers(token),
                      json={"title": title})
    return r.json().get("status") == "ok"

def save_doc(token, doc_id, content):
    r = requests.post(f"{BASE_URL}/api/doc/{doc_id}", headers=auth_headers(token),
                      json={"content": content, "status": "published"})
    data = r.json()
    if data.get("status") != "ok":
        print(f"保存文章失败: {data}")
        return False
    return True

def main():
    prog = get_progress()
    chapter = prog["chapter"] + 1

    if chapter > 60:
        print("全书已连载完毕！")
        sys.exit(0)

    chapter_file = os.path.join(NOVEL_DIR, f"ch{chapter:02d}.md")
    if not os.path.exists(chapter_file):
        print(f"找不到第{chapter}章文件: {chapter_file}")
        sys.exit(1)

    with open(chapter_file, encoding="utf-8") as f:
        lines = f.read().strip().split("\n", 1)
        title = lines[0].strip("# \t\r\n") if len(lines) > 0 else f"第{chapter}章"
        content = lines[1] if len(lines) > 1 else ""

    token = login()
    doc_id = create_doc(token)
    set_title(token, doc_id, title)
    ok = save_doc(token, doc_id, content)
    if ok:
        prog["chapter"] = chapter
        save_progress(prog)
        print(f"✅ 第{chapter}章「{title}」发布成功！")
    else:
        print(f"❌ 发布失败")

if __name__ == "__main__":
    main()
