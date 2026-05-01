# Fix index.html: full fix
with open('templates/index.html', 'r') as f:
    c = f.read()

# 1. Fix the extra closing braces
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
c = c.replace(""":root {
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
        }""",
    """":root {
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
        }""")

# 3. Warm theme dark-mode
c = c.replace("""body.dark-mode {
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
            --search-glow: rgba(59,130,246,0.2);
            --bell-bg: #1e293b;
            --bell-icon: #cbd5e1;
            --bell-gradient-start: #3b82f6;
            --bell-gradient-end: #00bf63;
            --avatar-bg: #2a2a4a;
        }""",
    """body.dark-mode {
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
        }""")

# 4. Font
c = c.replace("font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
              "font-family: 'Noto Serif SC', 'SimSun', 'STSong', '\u5b8b\u4f53', serif")

# 5. Button text color
c = c.replace("color: var(--text) !important;", "color: #000000 !important;")

# 6. Loading overlay HTML
c = c.replace('<div id="loadingOverlay"><div style="font-size: 1.5em; color: var(--text);">\u52a0\u8f7d\u4e2d...</div></div>',
    '<div id="loadingOverlay">\n            <div class="loader-title">\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</div>\n            <div class="loader-line"></div>\n        </div>')

# 7. Overlay CSS with transition
c = c.replace(
    '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n        }',
    '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n            transition: opacity 0.3s ease;\n        }')

# 8. Add loading CSS before user-list-item template literal
before_uli = c.find('.user-list-item')
loader_css = '\n@keyframes gradientShift {\n    0% { background-position: 200% 50%; }\n    100% { background-position: -200% 50%; }\n}\n.loader-title {\n    font-family: "Poppins", -apple-system, sans-serif;\n    font-size: 2.5em;\n    font-weight: 900;\n    letter-spacing: 0.15em;\n    background: linear-gradient(90deg, \n        rgba(255,255,255,0.3), \n        #ffffff 30%, #ffffff 70%,\n        rgba(255,255,255,0.3)\n    );\n    background-size: 200% 100%;\n    -webkit-background-clip: text;\n    background-clip: text;\n    color: transparent;\n    animation: gradientShift 2.5s ease-in-out infinite;\n    text-shadow: 0 0 30px rgba(255,255,255,0.1);\n    position: relative;\n    z-index: 10000;\n}\n.loader-line {\n    width: 120px;\n    height: 3px;\n    background: linear-gradient(90deg, \n        transparent, \n        rgba(255,255,255,0.8), \n        transparent\n    );\n    border-radius: 2px;\n    margin-top: 20px;\n    animation: gradientShift 2s ease-in-out infinite;\n    position: relative;\n    z-index: 10000;\n}\n'
c = c[:before_uli] + loader_css + c[before_uli:]

# 9. Add loading JS before main script
main_script = c.find('<script>\n        const')
loading_js = '<script>\n    // ===== \u52a0\u8f7d\u52a8\u753b =====\n    const PAGE_LOAD_TIME = Date.now();\n    const MIN_LOADING_DURATION = 2000;\n    let loadingHidden = false;\n    function hideLoadingOverlay() {\n        if (loadingHidden) return;\n        loadingHidden = true;\n        const overlay = document.getElementById(\'loadingOverlay\');\n        const elapsed = Date.now() - PAGE_LOAD_TIME;\n        const remaining = Math.max(0, MIN_LOADING_DURATION - elapsed);\n        setTimeout(() => {\n            overlay.style.opacity = \'0\';\n            setTimeout(() => {\n                overlay.style.display = \'none\';\n            }, 300);\n        }, remaining);\n    }\n</script>\n'
c = c[:main_script] + loading_js + c[main_script:]

# 10. Fallback timeout before checkLogin
c = c.replace('\n        checkLogin();', '\n        setTimeout(() => { if (!loadingHidden) hideLoadingOverlay(); }, 2500);\n        checkLogin();')

# Verification
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print("Brace depth:", d)
print("Loading JS:", "PAGE_LOAD_TIME" in c)
print("Gradient CSS:", "gradientShift" in c)
print("Loader HTML:", "loader-title" in c)
print("Warm theme:", "#fdf6ee" in c)
print("Dark mode:", "#1e1814" in c)
print("Noto Serif:", "Noto Serif SC" in c)
print("Button black:", "#000000 !important" in c)

with open('templates/index.html', 'w') as f:
    f.write(c)
print("Written!")
