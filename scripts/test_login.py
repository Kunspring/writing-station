#!/usr/bin/env python3
"""Playwright test - headless shell mode"""
from playwright.sync_api import sync_playwright
import time

def main():
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=True, args=['--no-sandbox'])
        p = b.new_page()
        
        # Capture errors
        js_errors = []
        p.on('pageerror', lambda e: js_errors.append(str(e)))
        
        print("=== STEP 1: 打开页面 ===")
        p.goto('http://localhost:5000/', timeout=8000, wait_until='networkidle')
        time.sleep(1.5)
        
        print("标题:", p.title())
        t = p.evaluate("localStorage.getItem('token')")
        print("token:", t)
        
        print("\n=== STEP 2: 登录 ===")
        p.fill('#loginUsername', 'misaka_mikoto')
        p.fill('#loginPassword', 'railgun10032')
        p.click('#loginBtn')
        time.sleep(2)
        
        t = p.evaluate("localStorage.getItem('token')")
        cu = p.evaluate("localStorage.getItem('currentUser')")
        print("token:", "有" if t else "无")
        print("currentUser:", "有" if cu else "无")
        print("主界面:", p.is_visible('#mainView:not(.hidden)'))
        
        if not t:
            print("❌ 登录失败")
            b.close()
            return
        
        print("\n=== STEP 3: 刷新 ===")
        p.reload(timeout=8000, wait_until='networkidle')
        time.sleep(2)
        
        t2 = p.evaluate("localStorage.getItem('token')")
        cu2 = p.evaluate("localStorage.getItem('currentUser')")
        print("token:", t2 if t2 else "NULL")
        print("currentUser:", cu2 if cu2 else "NULL")
        print("主界面:", p.is_visible('#mainView:not(.hidden)'))
        print("登录界面:", p.is_visible('#authView:not(.hidden)'))
        
        if t2 and p.is_visible('#mainView:not(.hidden)'):
            print("\n✅✅✅ 刷新后保持登录!")
        elif p.is_visible('#authView:not(.hidden)'):
            print("\n❌❌❌ 掉登录了!!")
        
        if js_errors:
            print("\n--- JS 错误 ---")
            for e in js_errors[:5]:
                print(" ", e)
        
        p.screenshot(path='/tmp/login_test.png')
        b.close()

if __name__ == '__main__':
    main()
