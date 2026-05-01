import re

with open('templates/index.html', 'r') as f:
    c = f.read()

# ===== STEP 1: Fix braces =====
depth = 0
removals = []
for i, ch in enumerate(c):
    if ch == '{': depth += 1
    elif ch == '}':
        depth -= 1
        if depth < 0:
            removals.append(i)
            depth = 0

for idx in sorted(removals, reverse=True):
    c = c[:idx] + c[idx+1:]

print(f"Removed {len(removals)} extra braces")

# ===== STEP 2: Warm theme CSS vars =====
# Light
c = c.replace(
    ':root { --bg: #fafbfc; --card-bg: #ffffff; --text: #1e1e2f; --border: #ddd; --primary: #0070f3; --primary-hover: #005bb5; --secondary: #6c757d; --secondary-hover: #5a6268; --shadow: rgba(0,0,0,0.05); --noti-bg: #ffffff; --comment-highlight: rgba(0,112,243,0.1); --search-bg: #f0f2f5; --search-glow: rgba(0,112,243,0.1); --bell-bg: #ffffff; --bell-icon: #777; --bell-gradient-start: #0070f3; --bell-gradient-end: #5ce1e6; --avatar-bg: #f0f2f5; }'
    .replace(' ', ''),
    ':root { --bg: #fdf6ee; --card-bg: #fffbf5; --text: #2d2418; --border: #e8ddd0; --primary: #d4a574; --primary-hover: #c4915a; --secondary: #a09080; --secondary-hover: #8a7a6a; --shadow: rgba(180,140,100,0.08); --noti-bg: #fffbf5; --comment-highlight: rgba(212,165,116,0.10); --search-bg: #f5ede2; --search-glow: rgba(212,165,116,0.10); --bell-bg: #fffbf5; --bell-icon: #a09080; --bell-gradient-start: #d4a574; --bell-gradient-end: #e8c9a0; --avatar-bg: #f5ede2; }'
    .replace(' ', '')
)
# Actually that won't work because the file has real newlines. Let me do a safer approach:

# Find :root block with proper newlines
root_match = re.search(r'        :root \{[^}]*\}', c)
if root_match:
    print(f"ROOT BLOCK: {root_match.group()[:100]}...")
    
    # Replace the root block values directly by key
    replacements = {
        '#fafbfc': '#fdf6ee',
        '#ffffff': '#fffbf5',
        '#1e1e2f': '#2d2418',
        '#ddd': '#e8ddd0',
        '#0070f3': '#d4a574',
        '#005bb5': '#c4915a',
        '#6c757d': '#a09080',
        '#5a6268': '#8a7a6a',
        'rgba(0,0,0,0.05)': 'rgba(180,140,100,0.08)',
        '#f0f2f5': '#f5ede2',
        'rgba(0,112,243,0.1)': 'rgba(212,165,116,0.10)',
        '#777': '#a09080',
        '5ce1e6': 'e8c9a0',
    }
    
    root_content = root_match.group()
    for old_val, new_val in replacements.items():
        if old_val in root_content:
            root_content = root_content.replace(old_val, new_val)
            print(f"  Replaced {old_val} -> {new_val}")
    
    c = c[:root_match.start()] + root_content + c[root_match.end():]
    print("Root vars replaced!")

# Dark
dark_match = re.search(r'body\.dark-mode \{.*?\n        \}', c, re.DOTALL)
if dark_match:
    dark_content = dark_match.group()
    print(f"\nDARK BLOCK: {dark_content[:200]}...")
    
    dark_repl = {
        '#1a1a2e': '#1e1814',
        '#16213e': '#2a221c',
        '#e0e0e0': '#ffffff',
        '#2a2a4a': '#3a3028',
        '#3b82f6': '#d4a574',
        '#2563eb': '#c4915a',
        '#4b5563': '#8a7a6a',
        '#374151': '#a09080',
        'rgba(0,0,0,0.3)': 'rgba(0,0,0,0.3)',
        '#1e293b': '#2a221c',
        'rgba(59,130,246,0.2)': 'rgba(212,165,116,0.15)',
        '#cbd5e1': '#a09080',
        '00bf63': 'e8c9a0',
    }
    
    for old_val, new_val in dark_repl.items():
        if old_val in dark_content:
            dark_content = dark_content.replace(old_val, new_val)
            print(f"  Replaced {old_val} -> {new_val}")
    
    # Add additional dark-mode vars
    if '--bg-color-card' not in dark_content:
        dark_content = dark_content.rstrip() + '\n            --bg-color-card: #2a221c;\n            --bg-color-alt: #a09080;\n            --font-color: #e8ddd0;\n            --main-color: #e8ddd0;\n        }'
    
    c = c[:dark_match.start()] + dark_content + c[dark_match.end():]
    print("Dark vars replaced!")

# ===== STEP 3: Font =====
c = c.replace(
    "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    "font-family: 'Noto Serif SC', 'SimSun', 'STSong', '\u5b8b\u4f53', serif"
)

# ===== STEP 4: Button black =====
c = c.replace(
    "color: #606060;\n            text-shadow: 0 1px #fff;",
    "color: #000000 !important;\n            text-shadow: none;"
)

# ===== STEP 5: Loading overlay HTML =====
old_overlay = '<div id="loadingOverlay"><div style="font-size: 1.5em; color: var(--text);">\u52a0\u8f7d\u4e2d...</div></div>'
new_overlay = '<div id="loadingOverlay"><div class="loader-title">\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</div><div class="loader-line"></div></div>'
if old_overlay in c:
    c = c.replace(old_overlay, new_overlay)
    print("\nOverlay HTML replaced!")

# ===== STEP 6: Overlay CSS with transition =====
old_ocss = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n        }'
new_ocss = '#loadingOverlay {\n            position: fixed; top: 0; left: 0; width: 100%; height: 100%;\n            background: var(--bg); display: flex; justify-content: center; align-items: center;\n            z-index: 9999;\n            transition: opacity 0.3s ease;\n        }'
if old_ocss in c:
    c = c.replace(old_ocss, new_ocss)
    print("Overlay CSS transition added!")

# ===== STEP 7: Loader CSS after overlay CSS =====
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

# Find user-list-item (template literal CSS) and add before it
uli_pos = c.find('.user-list-item')
if uli_pos > 0:
    c = c[:uli_pos] + '\n' + loader_css + c[uli_pos:]
    print("Loader CSS inserted!")

# ===== STEP 8: Loading JS =====
# Find the first <script> tag after socket.io
socket_script = c.find('<script src="https://cdn.socket.io')
if socket_script > 0:
    socket_end = c.find('>', socket_script) + 1
    loading_js = '\n<script>\nconst PAGE_LOAD_TIME = Date.now();\nconst MIN_LOADING_DURATION = 2000;\nlet loadingHidden = false;\nfunction hideLoadingOverlay() {\n    if (loadingHidden) return;\n    loadingHidden = true;\n    const overlay = document.getElementById("loadingOverlay");\n    const elapsed = Date.now() - PAGE_LOAD_TIME;\n    const remaining = Math.max(0, MIN_LOADING_DURATION - elapsed);\n    setTimeout(() => {\n        overlay.style.opacity = "0";\n        setTimeout(() => {\n            overlay.style.display = "none";\n        }, 300);\n    }, remaining);\n}\nsetTimeout(() => { if (!loadingHidden) hideLoadingOverlay(); }, 2500);\n</script>'
    c = c[:socket_end] + loading_js + c[socket_end:]
    print("Loading JS added after socket.io script!")
else:
    # Try to find first <script> tag
    first_script = c.find('<script>')
    if first_script > 0:
        loading_js = '\n<script>\nconst PAGE_LOAD_TIME = Date.now();\nconst MIN_LOADING_DURATION = 2000;\nlet loadingHidden = false;\nfunction hideLoadingOverlay() {\n    if (loadingHidden) return;\n    loadingHidden = true;\n    const overlay = document.getElementById("loadingOverlay");\n    const elapsed = Date.now() - PAGE_LOAD_TIME;\n    const remaining = Math.max(0, MIN_LOADING_DURATION - elapsed);\n    setTimeout(() => {\n        overlay.style.opacity = "0";\n        setTimeout(() => {\n            overlay.style.display = "none";\n        }, 300);\n    }, remaining);\n}\nsetTimeout(() => { if (!loadingHidden) hideLoadingOverlay(); }, 2500);\n</script>\n'
        c = c[:first_script] + loading_js + c[first_script:]
        print("Loading JS added before first script!")

# Verify
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(f"\nBrace depth: {d}")
print(f"Warm light: {'#fdf6ee' in c}")
print(f"Warm dark: {'#1e1814' in c}")
print(f"Font: {'Noto Serif SC' in c}")
print(f"Btn: {'#000000 !important' in c}")
print(f"Loader CSS: {'gradientShift' in c}")
print(f"Loader HTML: {'loader-title' in c}")
print(f"Loading JS: {'PAGE_LOAD_TIME' in c}")

with open('templates/index.html', 'w') as f:
    f.write(c)
