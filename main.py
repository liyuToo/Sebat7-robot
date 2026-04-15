import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client

def run_sebat7_robot():
    # UPDATED URL from your Instagram screenshot
    url = "https://sebat67.wed2c.com" 
    cl = Client()
    
    try:
        print(f"📡 Connecting to {url}...")
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Finding the first product
        link_tag = soup.find('a', href=True)
        if not link_tag or "/product/" not in link_tag['href']:
            print("p❌ No products found on the homepage. Check the URL.")
            return
            
        product_url = f"https://sebat67.wed2c.com{link_tag['href']}"
        print(f"📦 Found product: {product_url}")
        
        # Gather images and details
        p_res = requests.get(product_url)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        name = p_soup.find('h1').text.strip()
        price = p_soup.find(class_='product-price').text.strip()
        
        image_paths = []
        img_tags = p_soup.find_all('img')
        for i, img in enumerate(img_tags):
            src = img.get('src') or img.get('data-src')
            if src and "product" in src and len(image_paths) < 5:
                full_url = src if src.startswith('http') else f"https:{src}"
                path = f"style_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(requests.get(full_url).content)
                image_paths.append(path)

        # Humanized Caption
        caption = (
            f"Obsessed with this new look... ✨\n\n"
            f"The {name[:50]} just dropped at sebat7 and the details are everything. "
            f"Swipe to see the different styles! ➡️\n\n"
            f"Only {price} — Link in bio to shop the collection. ♡\n\n"
            f"#sebat7 #NewArrival #StyleDetails #DailyEssentials"
        )

        print(f"🤖 Logging in as {os.getenv('INSTA_USER')}...")
        cl.login(os.getenv("INSTA_USER"), os.getenv("INSTA_PASS"))
        
        print("🚀 Uploading carousel with music...")
        cl.album_upload(image_paths, caption, audio_path="background.mp3" if os.path.exists("background.mp3") else None)
        
        for p in image_paths: os.remove(p)
        print("✅ SUCCESS: Post is now live on sebat7_store!")

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
