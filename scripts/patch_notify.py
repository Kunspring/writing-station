import re

with open('server.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 在 load_users/save_users 之后加入通知辅助函数
helper_code = '''
# --- 通知系统 ---
def add_notification(username, noti):
    users = load_users()
    if username not in users:
        return
    if 'notifications' not in users[username]:
        users[username]['notifications'] = []
    users[username]['notifications'].insert(0, {
        **noti,
        'id': str(uuid.uuid4()),
        'read': False,
        'timestamp': datetime.now().isoformat()
    })
    # 最多保留50条
    users[username]['notifications'] = users[username]['notifications'][:50]
    save_users(users)
'''

content = content.replace('def save_users(users):', 'def save_users(users):\n' + helper_code)

# 2. 在 /api/login 返回数据中加入未读通知数量
login_code = '''
    # 获取未读通知数
    unread = sum(1 for n in users[username].get('notifications', []) if not n.get('read', False))
    user_info = {
        "username": username,
        "nickname": users[username]["nickname"],
        "avatar": users[username].get("avatar"),
        "unread": unread
    }
'''
content = re.sub(r"user_info = \{[^}]+\}", login_code.replace('\n', '\n    '), content)

# 3. 增加获取/标记通知的API
api_code = '''
# --- 通知 API ---
@app.route("/api/notifications", methods=["GET"])
def get_notifications():
    username = g.username
    if not username:
        return jsonify([])
    users = load_users()
    return jsonify(users.get(username, {}).get('notifications', []))

@app.route("/api/notifications/read", methods=["POST"])
def mark_notifications_read():
    username = g.username
    if not username:
        return jsonify({"status": "error"}), 401
    users = load_users()
    if username in users:
        for n in users[username].get('notifications', []):
            n['read'] = True
        save_users(users)
    return jsonify({"status": "ok"})

@app.route("/api/notifications/count", methods=["GET"])
def unread_count():
    username = g.username
    if not username:
        return jsonify({"count": 0})
    users = load_users()
    unread = sum(1 for n in users.get(username, {}).get('notifications', []) if not n.get('read', False))
    return jsonify({"count": unread})
'''

content = content.replace('if __name__ == "__main__":', api_code + '\n\nif __name__ == "__main__":')

# 4. 在回复评论、点赞时触发通知
# 4a 回复评论：在 add_comment 里判断 parentId 存在且评论者与父评论者不同则推送
reply_trigger = '''
        if parent_id:
            # 找到父评论作者
            for c in comments:
                if c["id"] == parent_id and c["username"] != username:
                    add_notification(c["username"], {
                        "type": "reply",
                        "from_user": nickname,
                        "from_avatar": users.get(username, {}).get("avatar"),
                        "doc_id": doc_id,
                        "comment_id": new_comment["id"],
                        "content": comment_text[:50]
                    })
'''
content = re.sub(r'(comments\.append\(new_comment\))', r'\1' + reply_trigger, content)

# 4b 点赞时：like_comment 里，点赞人不是评论作者时推送
like_trigger = '''
            if action == "liked" and c["username"] != username:
                add_notification(c["username"], {
                    "type": "like",
                    "from_user": nickname,
                    "from_avatar": users.get(username, {}).get("avatar"),
                    "doc_id": doc_id,
                    "comment_id": comment_id,
                    "content": c["comment"][:50]
                })
'''
content = re.sub(r"c\[\"likes\"\] = likes\s+save_comments\(doc_id, comments\)", r'\g<0>' + like_trigger, content)

with open('server.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("server.py 已成功打补丁！")
