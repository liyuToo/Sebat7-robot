import os
import requests
import json
from bs4 import BeautifulSoup
from instagrapi import Client

def run_sebat7_robot():
    product_full_url = "https://sebat67.wed2c.com/s/1eewTgZGS00" 
    cl = Client()
    # Path to save login session
    session_file = "insta_session.json"
    
    try:
        # 1. LOAD SESSION IF IT EXISTS
        if os.path.exists(session_file):
            print("🔄 Loading existing session...")
            cl.load_settings(session_file)

        user = os.getenv("INSTA_USER")
        pw = os.getenv("INSTA_PASS")

        print(f"🤖 Attempting login for {user}...")
        
        # 2. LOGIN WITH SMART ERROR HANDLING
        try:
            cl.login(user, pw)
        except Exception as e:
            if "checkpoint_required" in str(e) or "challenge_required" in str(e):
                print("⚠️ Challenge Required: Please check your Instagram app and tap 'This Was Me'.")
                return
            else:
                print(f"❌ Login failed: {e}")
                # If IP is blocked, we try a softer login approach
                cl.set_proxy("http://username:password@proxy_address:port") # Optional for later
                return

        # Save session for next time
        cl.dump_settings(session_file)

        # 3. GET PRODUCT IMAGES
        print(f"📦 Scraping: {product_full_url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        p_res = requests.get(product_full_url, headers=headers)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        
        image_paths = []
        # Fallback image search
        meta_img = p_soup.find('meta', property="og:image")
        if meta_img:
            path = "style_0.jpg"
            with open(path, "wb") as f:
                f.write(requests.get(meta_img['content']).content)
            image_paths.append(path)

        if not image_paths:
            print("❌ No images found.")
            return

        # 4. UPLOAD
        caption = f"Available now at sebat7! ✨ ✨\n\nShop the link in bio. #sebat7"
        print("🚀 Finalizing upload...")
        cl.album_upload(image_paths, caption)
        print("✅ SUCCESS!")

    except Exception as e:
        print(f"❌ GLOBAL ERROR: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
