import os
import requests
from bs4 import BeautifulSoup
from instagrapi import Client

def run_sebat7_robot():
    # DIRECT LINK TO PRODUCT
    product_full_url = "https://sebat67.wed2c.com/s/1eewTgZGS00" 
    
    cl = Client()
    try:
        print(f"📦 Target Product: {product_full_url}")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        
        # Get Product Details
        p_res = requests.get(product_full_url, headers=headers)
        p_soup = BeautifulSoup(p_res.text, 'html.parser')
        
        # Find product name
        name_tag = p_soup.find('h1') or p_soup.find('title')
        name = name_tag.text.strip() if name_tag else "New Arrival"
        
        # Gather all product images
        image_paths = []
        # Finding images in the common wed2c galleries
        img_tags = p_soup.find_all('img')
        for i, img in enumerate(img_tags):
            src = img.get('src') or img.get('data-src')
            # Filter for product images (usually large and from the same domain)
            if src and "product" in src and len(image_paths) < 5:
                full_url = src if src.startswith('http') else f"https:{src}"
                path = f"style_{i}.jpg"
                with open(path, "wb") as f:
                    f.write(requests.get(full_url).content)
                image_paths.append(path)

        if not image_paths:
            print("❌ Error: No images found. Trying fallback...")
            # If no images found, we check the meta tags
            meta_img = p_soup.find('meta', property="og:image")
            if meta_img:
                path = "style_main.jpg"
                with open(path, "wb") as f:
                    f.write(requests.get(meta_img['content']).content)
                image_paths.append(path)
            else:
                print("❌ Failed to find any images.")
                return

        print(f"🤖 Logging in to Instagram as {os.getenv('INSTA_USER')}...")
        cl.login(os.getenv("INSTA_USER"), os.getenv("INSTA_PASS"))
        
        caption = (
            f"Details matter... ✨\n\n"
            f"Discover the {name} now at sebat7. "
            f"Swipe to see why this is a collection favorite! ➡️\n\n"
            f"🔗 Shop the link in our bio. ♡\n\n"
            f"#sebat7 #ShopOnline #StyleInspiration #Quality"
        )
        
        print(f"🚀 Uploading carousel with {len(image_paths)} photos...")
        cl.album_upload(
            image_paths, 
            caption, 
            audio_path="background.mp3" if os.path.exists("background.mp3") else None
        )
        print("✅ SUCCESS: Post is live on sebat7_store!")

        # Clean up images
        for p in image_paths:
            if os.path.exists(p): os.remove(p)

    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    run_sebat7_robot()
