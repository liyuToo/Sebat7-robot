import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client

def run_sebat7_robot():
    url = "https://sebat67.wed2c.com" 
    cl = Client()
    
    try:
        print(f"📡 Connecting to {url}...")
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Look for ANY link that contains "product"
        all_links = soup.find_all('a', href=True)
        product_link = None
        for link in all_links:
            if "/product/" in link['href']:
                product_link = link['href']
                break
        
        if not product_link:
            print("❌ Error: Could not find any products. Site structure might be hidden.")
            return
            
        product_full_url = product_link if product_link.startswith('http') else f"https://sebat67.wed2c.com{product_link}"
        print(f"📦 Found Product: {product_full_url}")
        
        # Get Product Details
        p_res = requests.get(product_full_url, headers=headers)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        
        name = p_soup.find('h1').text.strip() if p_soup.find('h1') else "New Arrival"
        # Gather all images
        image_paths = []
        img_tags = p_soup.find_all('img')
        for i, img in enumerate(img_tags):
            src = img.get('src') or img.get('data-src')
            if src and "product" in src and len(image_paths) < 4:
                full_url = src if src.startswith('http') else f"https:{src}"
                path = f"style_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(requests.get(full_url).content)
                image_paths.append(path)

        if not image_paths:
            print("❌ Error: No images found.")
            return

        print(f"🤖 Logging in as {os.getenv('INSTA_USER')}...")
        cl.login(os.getenv("INSTA_USER"), os.getenv("INSTA_PASS"))
        
        caption = f"The {name} is finally here at sebat7! ✨ Swipe to see the styles. 🔗 Link in bio. #sebat7 #style"
        
        print("🚀 Uploading to Instagram...")
        cl.album_upload(image_paths, caption, audio_path="background.mp3" if os.path.exists("background.mp3") else None)
        print("✅ SUCCESS!")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
