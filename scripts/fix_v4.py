"""Fix index.html from bak2 properly"""
with open('templates/index.html', 'r') as f:
    raw = f.read()

# Strategy: Parse the file, fix its structural HTML issues,
# then apply theme changes

# Step 1: Remove extra closing braces
lines = raw.split('\n')
# Track depth, mark lines with extra }
depth = 0
fixed_lines = []
for line in lines:
    stripped = line.strip()
    # Count braces in this line
    open_b = stripped.count('{')
    close_b = stripped.count('}')
    
    new_depth = depth + open_b - close_b
    if new_depth < 0:
        # Extra closing braces - remove as many as needed
        extra = -new_depth
        while extra > 0 and close_b > 0:
            # Remove one } from this line
            idx = line.rfind('}')
            if idx >= 0:
                line = line[:idx] + line[idx+1:]
            close_b -= 1
            extra -= 1
            new_depth += 1
        new_depth = 0
    
    depth = new_depth
    fixed_lines.append(line)

c = '\n'.join(fixed_lines)
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(f"Brace depth after fix: {d}")

# Step 2: Add missing <head>, </style> if missing
# The structure should be: <!DOCTYPE html><html><head>...style...</style></head><body>...script...</script></body></html>

style_start = c.find('<style>')
if style_start >= 0:
    # Check if </style> exists
    style_end = c.find('</style>')
    if style_end < 0:
        # Find where CSS actually ends - look for @media or other elements
        # The CSS likely ends right before the first non-CSS block
        # Look for '--avatar-bg:' as the last CSS variable
        last_var = c.rfind(';', style_start, c.find('body.dark-mode'))
        
        # Find @media block which is the first thing after CSS variables  
        media_idx = c.find('@media (min-width: 600px)', style_start)
        
        if media_idx > 0:
            # Insert </style></head><body> before @media
            c = c[:media_idx] + '</style>\n</head>\n<body>\n' + c[media_idx:]
        else:
            # Insert after dark-mode curly brace
            dark_end = c.find('}\n', c.find('body.dark-mode'))
            if dark_end > 0:
                c = c[:dark_end+1] + '\n</style>\n</head>\n<body>\n' + c[dark_end+1:]
        
        print("Added </style></head><body>")

# Step 3: Add <script> if missing - find where JS code starts
# Look for the first JS keyword after <body>
body_start = c.find('<body>')
if body_start >= 0 and '<script>' not in c[body_start:]:
    # JS starts with 'const themeCheckbox' or 'function checkLogin' - find it
    for kw in ['const themeCheckbox', 'let currentUser', 'function checkLogin']:
        kw_idx = c.find(kw, body_start)
        if kw_idx > 0:
            # Check it's not inside a script tag already
            before = c[max(0,kw_idx-15):kw_idx]
            if 'script>' not in before:
                c = c[:kw_idx] + '<script>\n' + c[kw_idx:]
                print(f"Added <script> before '{kw}'")
                break

# Step 4: Add </script> if missing  
body_end = c.find('</body>')
if body_end > 0 and '</script>' not in c[body_start:body_end]:
    # Find checkLogin() as the last JS call
    ck_idx = c.rfind('checkLogin()', body_start, body_end)
    if ck_idx > 0:
        line_end = c.find('\n', ck_idx)
        c = c[:line_end+1] + '</script>\n' + c[line_end+1:]
        print("Added </script>")

# Step 5: Apply warm theme
# Replace light CSS variables
for old, new in [
    ('#fafbfc', '#fdf6ee'),
    ('#ffffff', '#fffbf5'),
    ('#1e1e2f', '#2d2418'),
    ('#ddd', '#e8ddd0'),
    ('#0070f3', '#d4a574'),
    ('#005bb5', '#c4915a'),
    ('#6c757d', '#a09080'),
    ('#5a6268', '#8a7a6a'),
    ('rgba(0,0,0,0.05)', 'rgba(180,140,100,0.08)'),
    ('#f0f2f5', '#f5ede2'),
    ('rgba(0,112,243,0.1)', 'rgba(212,165,116,0.10)'),
    ('#777', '#a09080'),
]:
    # Only replace within :root block
    root_start = c.find(':root {')
    root_end = c.find('body.dark-mode')
    root_block = c[root_start:root_end]
    if old in root_block:
        c = c[:root_start] + root_block.replace(old, new) + c[root_end:]
        root_block = root_block.replace(old, new)

# Replace dark CSS variables
for old, new in [
    ('#1a1a2e', '#1e1814'),
    ('#16213e', '#2a221c'),
    ('#e0e0e0', '#ffffff'),
    ('#2a2a4a', '#3a3028'),
    ('#3b82f6', '#d4a574'),
    ('#2563eb', '#c4915a'),
    ('#4b5563', '#8a7a6a'),
    ('#374151', '#a09080'),
    ('#1e293b', '#2a221c'),
    ('#cbd5e1', '#a09080'),
    ('#00bf63', '#e8c9a0'),
]:
    dark_start = c.find('body.dark-mode {')
    dark_end = c.find('}', c.find('}', dark_start) + 1) + 1
    dark_block = c[dark_start:dark_end]
    if old in dark_block:
        c = c[:dark_start] + dark_block.replace(old, new) + c[dark_end:]
        dark_block = dark_block.replace(old, new)

# Add additional dark-mode vars
if 'bg-color-card' not in dark_block:
    extra_vars = '\n            --bg-color-card: #2a221c;\n            --bg-color-alt: #a09080;\n            --font-color: #e8ddd0;\n            --main-color: #e8ddd0;'
    dark_block += extra_vars
    c = c[:dark_start] + dark_block + c[dark_end:]

# Step 6: Font
c = c.replace(
    "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif",
    "font-family: 'Noto Serif SC', 'SimSun', 'STSong', '\u5b8b\u4f53', serif"
)

# Step 7: Button black
c = c.replace(
    "color: #606060;\n            text-shadow: 0 1px #fff;",
    "color: #000000 !important;\n            text-shadow: none;"
)

# Verify
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(f"\nFinal brace depth: {d}")
print(f"<body>: {'<body>' in c}")
print(f"</body>: {'</body>' in c}")
print(f"<script>: {'<script>' in c and '</script>' in c}")
print(f"<style>: {'<style>' in c and '</style>' in c}")
print(f"Functions check:")
import re
funcs = re.findall(r'function \w+', c)
for f in funcs:
    print(f"  {f}")

with open('templates/index.html', 'w') as f:
    f.write(c)
