#!/usr/bin/env python3
"""Use route interception with synchronous wrapper"""
import sys, os, time
import subprocess, json

os.environ['DISPLAY'] = ':99'

from playwright.sync_api import sync_playwright

# Read the patched HTML
patched_html = open('/tmp/index_patched.html').read()

with sync_playwright() as pw:
    b = pw.chromium.launch(
        headless=False,
        executable_path='/root/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome',
        args=['--no-sandbox', '--disable-gpu']
    )
    ctx = b.new_context()
    
    # Route interception - must use async handler
    # Playwright sync API supports this: we define async handler in a sync context
    
    p = ctx.new_page()
    
    # Set up route before loading
    def route_handler(route):
        url = route.request.url
        if url.endswith('/') or 'index.html' in url:
            route.fulfill(body=patched_html, content_type='text/html; charset=utf-8')
        else:
            route.continue_()
    
    # Register the route handler (sync version - playwright handles it)
    p.route('**/*', route_handler)
    
    logs = []
    p.on('console', lambda msg: logs.append((msg.type, msg.text)))
    p.on('pageerror', lambda err: logs.append(("PAGE_ERR", str(err))))
    p.on('response', lambda resp: logs.append(("RESP", f"{resp.status} {resp.url}")))
    
    p.goto('http://localhost:5000/', timeout=8000)
    print("Loaded:", p.title())
    time.sleep(1)
    
    # Login
    print("LOGGING IN...")
    p.evaluate("""
        async () => {
            const res = await fetch('/api/login', {method:'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username: 'misaka_mikoto', password: 'railgun10032'})});
            const data = await res.json();
            if (data.status === 'ok') {
                localStorage.setItem('token', data.token);
                localStorage.setItem('currentUser', JSON.stringify(data.user));
            }
        }
    """)
    time.sleep(1)
    
    # Reload (should get patched HTML)
    print("RELOADING...")
    p.goto('http://localhost:5000/', timeout=8000)
    time.sleep(3)
    
    r = p.evaluate("() => { let av=document.getElementById('authView'), mv=document.getElementById('mainView'); return {authDisp:window.getComputedStyle(av).display, mainDisp:window.getComputedStyle(mv).display}; }")
    print("FINAL:", r)
    
    print("\n=== TRACE-CL LOGS ===")
    for ltype, msg in logs:
        if 'TRACE-CL' in msg:
            print(f"  {msg}")
    print("\n=== OTHER LOGS ===")
    for ltype, msg in logs:
        if 'TRACE-CL' not in msg and ('ERR' in ltype or 'error' in ltype.lower()):
            print(f"[{ltype}] {msg[:300]}")
    
    b.close()
