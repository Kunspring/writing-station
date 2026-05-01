# Fix index.html: repair braces, apply warm theme + loading animation
with open('templates/index.html', 'r') as f:
    c = f.read()

# Step 1: Fix brace issues
depth = 0
fixes = []
for i, ch in enumerate(c):
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth < 0:
            fixes.append(i)
            depth = 0

print(f"Found {len(fixes)} extra closing braces")
removed = 0
for idx in fixes:
    adj = idx - removed
    c = c[:adj] + c[adj+1:]
    removed += 1

if depth > 0:
    c += '}' * depth
    print(f"Added {depth} closing braces at end")

d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(f"Brace depth after fix: {d}")

# Step 2: Apply warm theme
light_old = """        :root {
            --bg: #fafbfc;
            --card-bg: #ffffff;
            --text: #1e1e2f;
            --border: #ddd;
            --primary: #0070f3;
            --primary-hover: #005bb5;
            --secondary: #6c757d;
            --secondary-hover: #5a6268;
            --shadow: rgba(0,0,0,0.05);
            --noti-bg: #ffffff;
            --comment-highlight: rgba(0,112,243,0.1);
            --search-bg: #f0f2f5;
            --search-glow: rgba(0,112,243,0.1);
            --bell-bg: #ffffff;
            --bell-icon: #777;
            --bell-gradient-start: #0070f3;
            --bell-gradient-end: #5ce1e6;
            --avatar-bg: #f0f2f5;
        }"""

light_new = """        :root {
            --bg: #fdf6ee;
            --card-bg: #fffbf5;
            --text: #2d2418;
            --border: #e8ddd0;
            --primary: #d4a574;
            --primary-hover: #c4915a;
            --secondary: #a09080;
            --secondary-hover: #8a7a6a;
            --shadow: rgba(180,140,100,0.08);
            --noti-bg: #fffbf5;
            --comment-highlight: rgba(212,165,116,0.10);
            --search-bg: #f5ede2;
            --search-glow: rgba(212,165,116,0.10);
            --bell-bg: #fffbf5;
            --bell-icon: #a09080;
            --bell-gradient-start: #d4a574;
            --bell-gradient-end: #e8c9a0;
            --avatar-bg: #f5ede2;
        }"""

dark_old = """body.dark-mode {
            --bg: #1a1a2e;
            --card-bg: #16213e;
            --text: #e0e0e0;
            --border: #2a2a4a;
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --secondary: #4b5563;
            --secondary-hover: #374151;
            --shadow: rgba(0,0,0,0.3);
            --noti-bg: #1e293b;
            --comment-highlight: rgba(0,112,243,0.15);
            --search-bg: #1e293b;
            --search-glow: rgba(0,112,243,0.15);
            --bell-bg: #1e293b;
            --bell-icon: #aaa;
            --bell-gradient-start: #3b82f6;
            --bell-gradient-end: #5ce1e6;
            --avatar-bg: #1e293b;
            --bg-color-card: #1e293b;
            --bg-color-alt: #aaa;
            --font-color: #e0e0e0;
            --main-color: #e0e0e0;
        }"""

dark_new = """body.dark-mode {
            --bg: #1e1814;
            --card-bg: #2a221c;
            --text: #ffffff;
            --border: #3a3028;
            --primary: #d4a574;
            --primary-hover: #c4915a;
            --secondary: #8a7a6a;
            --secondary-hover: #a09080;
            --shadow: rgba(0,0,0,0.3);
            --noti-bg: #2a221c;
            --comment-highlight: rgba(212,165,116,0.15);
            --search-bg: #2a221c;
            --search-glow: rgba(212,165,116,0.15);
            --bell-bg: #2a221c;
            --bell-icon: #a09080;
            --bell-gradient-start: #d4a574;
            --bell-gradient-end: #e8c9a0;
            --avatar-bg: #2a221c;
            --bg-color-card: #2a221c;
            --bg-color-alt: #a09080;
            --font-color: #e8ddd0;
            --main-color: #e8ddd0;
        }"""

c = c.replace(light_old, light_new)
c = c.replace(dark_old, dark_new)

# Step 3: Fix button color to force black (NOT var(--text))
c = c.replace("color: var(--text) !important;", "color: #000000 !important;")

# Fix .create-btn too
c = c.replace("color: var(--text);", "color: #000000;")

# But only inside .basic-btn and .create-btn context
# Actually let's be more careful - let me just handle the known pattern

# Step 4: Fix font
c = c.replace(
    "body {\n            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    "body {\n            font-family: 'Noto Serif SC', 'SimSun', 'STSong', '\u5b8b\u4f53', serif"
)

# Step 5: Add loading overlay HTML
old_overlay = '<div id="loadingOverlay"><div style="font-size: 1.5em; color: var(--text);">\u52a0\u8f7d\u4e2d...</div></div>'
new_overlay = '''<div id="loadingOverlay">
            <div class="loader-title">\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</div>
            <div class="loader-line"></div>
        </div>'''
c = c.replace(old_overlay, new_overlay)

# Step 6: Add loading CSS before </style>
style_end = c.find('</style>')
css_block = '''
@keyframes gradientShift {
    0% { background-position: 200% 50%; }
    100% { background-position: -200% 50%; }
}
.loader-title {
    font-family: "Poppins", -apple-system, sans-serif;
    font-size: 2.5em;
    font-weight: 900;
    letter-spacing: 0.15em;
    background: linear-gradient(90deg, 
        rgba(255,255,255,0.3), 
        #ffffff 30%, #ffffff 70%,
        rgba(255,255,255,0.3)
    );
    background-size: 200% 100%;
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    animation: gradientShift 2.5s ease-in-out infinite;
    text-shadow: 0 0 30px rgba(255,255,255,0.1);
    position: relative;
    z-index: 10000;
}
.loader-line {
    width: 120px;
    height: 3px;
    background: linear-gradient(90deg, 
        transparent, 
        rgba(255,255,255,0.8), 
        transparent
    );
    border-radius: 2px;
    margin-top: 20px;
    animation: gradientShift 2s ease-in-out infinite;
    position: relative;
    z-index: 10000;
}
'''
c = c[:style_end] + css_block + '\n' + c[style_end:]

# Step 7: Add transition to overlay CSS
old_overlay_css = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n        }'
new_overlay_css = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n            transition: opacity 0.3s ease;\n        }'
c = c.replace(old_overlay_css, new_overlay_css)

# Step 8: Add loading JS right before the socket.io script tag
socket_script = '<script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>'
loading_js = '''<script>
    // ===== \u52a0\u8f7d\u52a8\u753b =====
    const PAGE_LOAD_TIME = Date.now();
    const MIN_LOADING_DURATION = 2000;
    let loadingHidden = false;
    function hideLoadingOverlay() {
        if (loadingHidden) return;
        loadingHidden = true;
        const overlay = document.getElementById('loadingOverlay');
        const elapsed = Date.now() - PAGE_LOAD_TIME;
        const remaining = Math.max(0, MIN_LOADING_DURATION - elapsed);
        setTimeout(() => {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.style.display = 'none';
            }, 300);
        }, remaining);
    }
</script>'''
c = c.replace(socket_script, loading_js + '\n    ' + socket_script)

# Step 9: Add hideLoading fallback before checkLogin()
check_login_call = '\n        checkLogin();'
fallback = '''
        // loading fallback
        setTimeout(() => {
            if (!loadingHidden) hideLoadingOverlay();
        }, 2500);
        checkLogin();'''
c = c.replace(check_login_call, fallback)

with open('templates/index.html', 'w') as f:
    f.write(c)

d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(f"Final brace depth: {d}")
print("Done!")
