import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client
import time

def run_sebat7_robot():
    url = "https://sebat7.wed2c.com"
    cl = Client()
    
    try:
        # 1. Scrape Store for latest product
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        link_tag = soup.find('a', href=True)
        if not link_tag: return
        product_url = f"https://sebat7.wed2c.com{link_tag['href']}"
        
        # 2. Extract Details & All Style Photos
        p_res = requests.get(product_url)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        name = p_soup.find('h1').text.strip()
        price = p_soup.find(class_='product-price').text.strip()
        
        # Gather images (Filter for actual product images)
        img_tags = p_soup.find_all('img')
        image_paths = []
        for i, img in enumerate(img_tags):
            src = img.get('src') or img.get('data-src')
            if src and "product" in src and len(image_paths) < 6:
                full_url = src if src.startswith('http') else f"https:{src}"
                path = f"style_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(requests.get(full_url).content)
                image_paths.append(path)

        # 3. Humanize the Caption (Max 350 Chars)
        caption = (
            f"Obsessed with this new look... ✨\n\n"
            f"The {name[:50]} just dropped at sebat7 and the details are everything. "
            f"Swipe to see the different styles! ➡️\n\n"
            f"Only {price} — Link in bio to shop the collection. ♡\n\n"
            f"#sebat7 #NewArrival #StyleDetails #DailyEssentials"
        )

        # 4. Login and Post Carousel with Music
        print(f"🤖 sebat7 Robot: Logging in...")
        cl.login(os.getenv("INSTA_USER"), os.getenv("INSTA_PASS"))
        
        music_path = "background.mp3" if os.path.exists("background.mp3") else None
        
        print(f"🚀 Uploading carousel with {len(image_paths)} photos...")
        cl.album_upload(
            image_paths, 
            caption,
            audio_path=music_path
        )
        
        # Cleanup
        for p in image_paths: os.remove(p)
        print("✅ Post Live on Instagram!")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
