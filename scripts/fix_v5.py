import re

with open('templates/index.html', 'r') as f:
    c = f.read()

# 1. Auth fetch
check_start = c.find('function checkLogin()')
auth_func = """function authFetch(url, options = {}) {
            const token = localStorage.getItem('token');
            if (token) {
                options.headers = {
                    ...options.headers,
                    'Authorization': 'Bearer ' + token
                };
            }
            return fetch(url, options);
        }

        """
c = c[:check_start] + auth_func + c[check_start:]

# 2. Loader CSS - one-liner to avoid indentation issues
loader_css = """/* From Uiverse.io by andrew-manzyk */
.loader { --main-size: 4em; --text-color: #ffffff; --shine-color: #ffffff40; --shadow-color: #aaaaaa; display: flex; justify-content: center; align-items: center; overflow: hidden; user-select: none; position: relative; font-size: var(--main-size); font-weight: 900; text-transform: uppercase; color: var(--text-color); width: 7.3em; height: 1em; filter: drop-shadow(0 0 0.05em var(--shine-color)); }
.loader .text { display: flex; align-items: center; justify-content: center; text-align: center; white-space: nowrap; overflow: hidden; position: absolute; }
.loader .text:nth-child(1) { clip-path: polygon(0% 0%, 11.11% 0%, 11.11% 100%, 0% 100%); font-size: calc(var(--main-size) / 20); margin-left: -2.1em; opacity: 0.6; }
.loader .text:nth-child(2) { clip-path: polygon(11.11% 0%, 22.22% 0%, 22.22% 100%, 11.11% 100%); font-size: calc(var(--main-size) / 16); margin-left: -0.98em; opacity: 0.7; }
.loader .text:nth-child(3) { clip-path: polygon(22.22% 0%, 33.33% 0%, 33.33% 100%, 22.22% 100%); font-size: calc(var(--main-size) / 13); margin-left: -0.33em; opacity: 0.8; }
.loader .text:nth-child(4) { clip-path: polygon(33.33% 0%, 44.44% 0%, 44.44% 100%, 33.33% 100%); font-size: calc(var(--main-size) / 11); margin-left: -0.05em; opacity: 0.9; }
.loader .text:nth-child(5) { clip-path: polygon(44.44% 0%, 55.55% 0%, 55.55% 100%, 44.44% 100%); font-size: calc(var(--main-size) / 10); margin-left: 0em; opacity: 1; }
.loader .text:nth-child(6) { clip-path: polygon(55.55% 0%, 66.66% 0%, 66.66% 100%, 55.55% 100%); font-size: calc(var(--main-size) / 11); margin-left: 0.05em; opacity: 0.9; }
.loader .text:nth-child(7) { clip-path: polygon(66.66% 0%, 77.77% 0%, 77.77% 100%, 66.66% 100%); font-size: calc(var(--main-size) / 13); margin-left: 0.33em; opacity: 0.8; }
.loader .text:nth-child(8) { clip-path: polygon(77.77% 0%, 88.88% 0%, 88.88% 100%, 77.77% 100%); font-size: calc(var(--main-size) / 16); margin-left: 0.98em; opacity: 0.7; }
.loader .text:nth-child(9) { clip-path: polygon(88.88% 0%, 100% 0%, 100% 100%, 88.88% 100%); font-size: calc(var(--main-size) / 20); margin-left: 2.1em; opacity: 0.6; }
.loader .text span { animation: scrolling 2s cubic-bezier(0.1, 0.6, 0.9, 0.4) infinite, shadow 2s cubic-bezier(0.1, 0.6, 0.9, 0.4) infinite; }
.loader .text:nth-child(1) span { background: linear-gradient(to right, var(--text-color) 4%, var(--shadow-color) 7%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(2) span { background: linear-gradient(to right, var(--text-color) 9%, var(--shadow-color) 13%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(3) span { background: linear-gradient(to right, var(--text-color) 15%, var(--shadow-color) 18%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(4) span { background: linear-gradient(to right, var(--text-color) 20%, var(--shadow-color) 23%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(6) span { background: linear-gradient(to right, var(--shadow-color) 29%, var(--text-color) 32%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(7) span { background: linear-gradient(to right, var(--shadow-color) 34%, var(--text-color) 37%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(8) span { background: linear-gradient(to right, var(--shadow-color) 39%, var(--text-color) 42%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .text:nth-child(9) span { background: linear-gradient(to right, var(--shadow-color) 45%, var(--text-color) 48%); background-size: 200% auto; -webkit-background-clip: text; background-clip: text; color: transparent; }
.loader .line { position: relative; display: flex; align-items: center; justify-content: center; overflow: hidden; height: 0.05em; width: calc(var(--main-size) / 2); margin-top: 0.9em; border-radius: 0.05em; }
@keyframes wobble { 0% { transform: translateX(-90%); } 50% { transform: translateX(90%); } 100% { transform: translateX(-90%); } }
@keyframes scrolling { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
@keyframes shadow { 0% { background-position: -98% 0; } 100% { background-position: 102% 0; } }
"""

overlay_css_idx = c.find('#loadingOverlay {')
if overlay_css_idx > 0:
    c = c[:overlay_css_idx] + loader_css + '\n' + c[overlay_css_idx:]
    print("1. Loader CSS added")

# 3. Overlay HTML
old_overlay = '<div id="loadingOverlay"><div style="font-size: 1.5em; color: var(--text);">\u52a0\u8f7d\u4e2d...</div></div>'
new_overlay = """<div id="loadingOverlay">
        <!-- From Uiverse.io by andrew-manzyk -->
        <div class="loader">
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="text"><span>\u672b\u65e5\u56de\u54cd\u51fa\u7248\u793e</span></div>
         <div class="line"></div>
        </div>
    </div>"""
if old_overlay in c:
    c = c.replace(old_overlay, new_overlay)
    print("2. Overlay HTML replaced")
else:
    print("2. WARN: Overlay NOT FOUND")
    # debug
    ov = c.find('loadingOverlay')
    print(f"   found at {ov}: {repr(c[ov:ov+150])}")

# 4. Loading JS
socket_script = '<script src="https://cdn.socket.io/4.5.0/socket.io.min.js"></script>'
loading_js = """<script>
const PAGE_LOAD_TIME = Date.now();
const MIN_LOADING_DURATION = 2000;
let loadingHidden = false;
function hideLoadingOverlay() {
    if (loadingHidden) return;
    loadingHidden = true;
    const overlay = document.getElementById("loadingOverlay");
    const elapsed = Date.now() - PAGE_LOAD_TIME;
    const remaining = Math.max(0, MIN_LOADING_DURATION - elapsed);
    setTimeout(() => {
        overlay.style.opacity = "0";
        setTimeout(() => {
            overlay.style.display = "none";
        }, 300);
    }, remaining);
}
</script>
"""
if socket_script in c:
    c = c.replace(socket_script, socket_script + '\n' + loading_js)
    print("3. Loading JS added")

# 5. Remove overlay display=none in checkLogin
c = re.sub(r'\n\s+document\.getElementById\(\'loadingOverlay\'\)\.style\.display = \'none\';', '', c)

# 6. Fallback timeout
c = c.replace('\n        checkLogin();', '\n        setTimeout(() => { if (!loadingHidden) hideLoadingOverlay(); }, 2500);\n        checkLogin();')
print("4. Fallback added")

# Verify
d = 0
for ch in c:
    if ch == '{': d+=1
    elif ch == '}': d-=1
print(print(f'Brace: {d}'))
print(f"Scrolling: {'@keyframes scrolling' in c}")
print(f"Loader: {'class=\"loader\"' in c}")
print(f"JS: {'PAGE_LOAD_TIME' in c}")
print(f"showAuth: {'showAuth' in c}")
print(f"handleLogin: {'handleLogin' in c}")
print(f"authFetch: {'function authFetch' in c}")

with open('templates/index.html', 'w') as f:
    f.write(c)
