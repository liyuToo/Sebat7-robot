import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client

def run_sebat7_robot():
    product_full_url = "https://sebat67.wed2c.com/s/1eewTgZGS00" 
    cl = Client()
    
    try:
        print(f"📦 Target Product: {product_full_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        
        p_res = requests.get(product_full_url, headers=headers)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        
        # 1. Get Images from EVERY possible source on the page
        image_paths = []
        # Check meta tags first (best quality)
        meta_img = p_soup.find('meta', property="og:image")
        if meta_img:
            img_url = meta_img['content']
            with open("style_0.jpg", "wb") as f:
                f.write(requests.get(img_url).content)
            image_paths.append("style_0.jpg")

        # Search for other product photos
        all_imgs = p_soup.find_all('img')
        for i, img in enumerate(all_imgs):
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src and "product" in src and len(image_paths) < 4:
                full_url = src if src.startswith('http') else f"https:{src}"
                if full_url not in [img_url if meta_img else ""]:
                    path = f"style_{i+1}.jpg"
                    with open(path, "wb") as f:
                        f.write(requests.get(full_url).content)
                    image_paths.append(path)

        if not image_paths:
            print("❌ Error: No images found.")
            return

        # 2. Login using the Secrets we just set
        user = os.getenv("INSTA_USER")
        pw = os.getenv("INSTA_PASS")
        
        if not user or not pw:
            print("❌ ERROR: Username or Password missing in GitHub Secrets!")
            return

        print(f"🤖 Logging in as {user}...")
        cl.login(user, pw)
        
        caption = (
            f"Precision meets power. 🛠️✨\n\n"
            f"The Automotive Multifunctional Detector is a game-changer for your garage. "
            f"Professional grade, now available at sebat7. ➡️\n\n"
            f"🔗 Click the link in our bio to order yours today! ♡\n\n"
            f"#sebat7 #AutomotiveTech #GarageTools #Innovation"
        )
        
        print(f"🚀 Uploading {len(image_paths)} photos...")
        cl.album_upload(image_paths, caption, audio_path="background.mp3" if os.path.exists("background.mp3") else None)
        print("✅ SUCCESS: The post is live!")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
