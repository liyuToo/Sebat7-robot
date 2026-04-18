from instagrapi import Client

cl = Client()
# This makes the robot look like a Samsung phone instead of a server
cl.set_user_agent("Instagram 269.0.0.18.75 Android (26/8.0.0; 480dpi; 1080x1920; Samsung; SM-G950F; dreamlte; samsungexynos8895; en_US; 444062322)")

try:
    print("🤖 Attempting clean login...")
    cl.login("sebat7_store", "YOUR_NEW_PASSWORD")
    cl.dump_settings("insta_session.json")
    print("✅ SUCCESS! Session created.")
except Exception as e:
    print(f"❌ Still blocked: {e}")
