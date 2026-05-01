import requests
from datetime import datetime
import pytz
import re

# স্পোর্টস সোর্স ইউআরএলগুলো
urls = [
    "https://raw.githubusercontent.com/srhady/crichd-speical-live-event/refs/heads/main/Go_Live_Events.m3u",
    "https://raw.githubusercontent.com/srhady/crichd-speical-live-event/refs/heads/main/Live_Events.m3u",
    "https://raw.githubusercontent.com/srhady/crichd-speical-live-event/refs/heads/main/Crichdat_Live.m3u"
]

# IBS TV app promotion ভিডিও
IBS_PROMO_VIDEO = "https://raw.githubusercontent.com/ibstvofficial/IBS-TV-special-movies.m3u/refs/heads/main/promo%20dual.mp4"

def clean_sports_name(name):
    junk = ["| High Quality", "| BDIX", "| VIP", "SD", "HD", "FHD", "(Backup)", "Premium", "1080p", "720p"]
    for word in junk:
        name = name.replace(word, "")
    return name.strip()

def normalize_group(group_name):
    group_name = group_name.upper()
    if any(x in group_name for x in ["SPORTS", "CRICKET", "LIVE", "FOOTBALL"]):
        return "LIVE SPORTS"
    if any(x in group_name for x in ["BANGLA", "BD"]):
        return "LIVE TV"
    return "SPORTS EVENTS"

def create_sports_playlist():
    bd_tz = pytz.timezone('Asia/Dhaka')
    current_time = datetime.now(bd_tz).strftime('%I:%M %p %d-%m-%Y')

    merged_content = f"""#EXTM3U
# Playlist Name: Crichd Live Sports
# Last Update: {current_time} (BD Time)
# Owner: Md. Sakib Hasan
# Telegram: https://t.me/bdixiptvbd\n"""

    DEFAULT_LOGO = "https://bdixiptvbd.com/logo.png"
    seen_links = set()
    added_groups = set()

    for url in urls:
        try:
            print(f"Fetching from: {url}")
            response = requests.get(url, timeout=25)
            if response.status_code == 200:
                content = response.text
                
                # M3U ফাইলের প্রতিটি চ্যানেল ব্লক আলাদা করার জন্য রেগুলার এক্সপ্রেশন
                matches = re.findall(r'(#EXTINF:[^\n]*)\n(https?://[^\n]+)', content)
                
                for extinf, stream_url in matches:
                    stream_url = stream_url.strip()
                    if stream_url and stream_url not in seen_links:
                        group_match = re.search(r'group-title="([^"]+)"', extinf)
                        raw_group = group_match.group(1) if group_match else "LIVE SPORTS"
                        final_group = normalize_group(raw_group)

                        logo_match = re.search(r'tvg-logo="([^"]+)"', extinf)
                        final_logo = logo_match.group(1) if (logo_match and logo_match.group(1)) else DEFAULT_LOGO

                        name_part = extinf.split(",")[-1]
                        final_name = clean_sports_name(name_part)

                        # প্রমোশন যোগ করার লজিক
                        if final_group not in added_groups:
                            promo_line = f'#EXTINF:-1 tvg-logo="{DEFAULT_LOGO}" group-title="{final_group}",--- [ {final_group} PROMO ] ---'
                            merged_content += promo_line + "\n" + IBS_PROMO_VIDEO + "\n"
                            added_groups.add(final_group)

                        new_line = f'#EXTINF:-1 tvg-logo="{final_logo}" group-title="{final_group}",{final_name}'
                        merged_content += new_line + "\n" + stream_url + "\n"
                        seen_links.add(stream_url)
                        
        except Exception as e:
            print(f"Error fetching sports: {e}")

    try:
        with open("Crichd playlist.m3u", "w", encoding="utf-8") as f:
            f.write(merged_content)
        print(f"Success! Crichd playlist.m3u updated at {current_time}")
    except Exception as e:
        print(f"Save Error: {e}")

if __name__ == "__main__":
    create_sports_playlist()
                  
