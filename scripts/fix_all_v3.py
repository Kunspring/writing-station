# Fix index.html: full fix v3 - check every replacement
with open('templates/index.html', 'r') as f:
    c = f.read()

# 1. Fix extra closing braces
depth = 0
removals = set()
for i, ch in enumerate(c):
    if ch == '{':
        depth += 1
    elif ch == '}':
        depth -= 1
        if depth < 0:
            removals.add(i)
            depth = 0

for idx in sorted(removals, reverse=True):
    c = c[:idx] + c[idx+1:]

# 2. Warm theme :root 
# Match the actual content from .bak2
old_light = """        :root {
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
new_light = """        :root {
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

assert old_light in c, "LIGHT THEME NOT FOUND!"
c = c.replace(old_light, new_light)
print("1. Light theme replaced")

# 3. Dark mode
old_dark = """body.dark-mode {
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
            --search-bg: #1e293b;
            --search-glow: rgba(59,130,246,0.2);
            --bell-bg: #1e293b;
            --bell-icon: #cbd5e1;
            --bell-gradient-start: #3b82f6;
            --bell-gradient-end: #00bf63;
            --avatar-bg: #2a2a4a;
        }"""
new_dark = """body.dark-mode {
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

assert old_dark in c, "DARK THEME NOT FOUND!"
c = c.replace(old_dark, new_dark)
print("2. Dark theme replaced")

# 4. Font
old_font = "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif"
new_font = "font-family: 'Noto Serif SC', 'SimSun', 'STSong', '\u5b8b\u4f53', serif"
assert old_font in c, "FONT NOT FOUND!"
c = c.replace(old_font, new_font)
print("3. Font replaced")

# 5. Button text - .basic-btn color is #606060, change to #000000
old_btn = """color: #606060;
            text-shadow: 0 1px #fff;"""
new_btn = """color: #000000 !important;
            text-shadow: none;"""
assert old_btn in c, "BUTTON COLOR NOT FOUND!"
c = c.replace(old_btn, new_btn)
print("4. Button color replaced")

# 6. Loading overlay HTML
old_overlay = '<div id="loadingOverlay"><div style="font-size: 1.5em; color: var(--text);">\u52a0\u8f7d\u4e2d...</div></div>'
new_overlay = '<div id="loadingOverlay">\n            <div class="loader-title">\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</div>\n            <div class="loader-line"></div>\n        </div>'
assert old_overlay in c, "OVERLAY HTML NOT FOUND!"
c = c.replace(old_overlay, new_overlay)
print("5. Overlay HTML replaced")

# 7. Overlay CSS with transition
old_ocss = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n        }'
new_ocss = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n            transition: opacity 0.3s ease;\n        }'
assert old_ocss in c, "OVERLAY CSS NOT FOUND!"
c = c.replace(old_ocss, new_ocss)
print("6. Overlay CSS with transition")

# 8. Loading CSS before user-list-item template literal
loader_css = """@keyframes gradientShift {
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
"""

before_uli = c.find('.user-list-item')
assert before_uli > 0, "USER LIST ITEM NOT FOUND!"
c = c[:before_uli] + '\n' + loader_css + c[before_uli:]
print("7. Loading CSS added")

# 9. Loading JS before main script
main_script = c.find('<script>\n        const')
loading_js = """<script>
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
</script>
"""
assert main_script > 0, "MAIN SCRIPT NOT FOUND!"
c = c[:main_script] + loading_js + c[main_script:]
print("8. Loading JS added")

# 10. Fallback timeout before checkLogin
assert '\n        checkLogin();' in c, "CHECKLOGIN NOT FOUND!"
c = c.replace('\n        checkLogin();', '\n        setTimeout(() => { if (!loadingHidden) hideLoadingOverlay(); }, 2500);\n        checkLogin();')
print("9. Fallback timeout added")

# Verification
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print("")
print("=== VERIFICATION ===")
print(f"Brace depth: {d}")
print(f"Loading JS: {'PAGE_LOAD_TIME' in c}")
print(f"Gradient CSS: {'gradientShift' in c}")
print(f"Loader HTML: {'loader-title' in c}")
print(f"Warm theme: {'#fdf6ee' in c}")
print(f"Dark mode: {'#1e1814' in c}")
print(f"Noto Serif: {'Noto Serif SC' in c}")
print(f"Button black: {'#000000 !important' in c}")

with open('templates/index.html', 'w') as f:
    f.write(c)
print("Written!")
