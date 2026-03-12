import os
from icrawler.builtin import GoogleImageCrawler

PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
IMAGE_DUMP = os.path.join(PROJECT_ROOT, "dump_zone", "player_images")

def fetch_player_image(player_name):
    """fetches one image for the player and returns the path."""
    if not player_name or player_name.lower() == "unknown":
        return None
    
    # clean name for folder
    save_path = os.path.join(IMAGE_DUMP, player_name.replace(" ", "_").lower())
    os.makedirs(save_path, exist_ok=True)

    google_crawler = GoogleImageCrawler(storage={'root_dir': save_path})
    # filter for 'face' to get better player portraits
    google_crawler.crawl(keyword=f"{player_name} chess player face", max_num=1)
    
    # icrawler saves as 000001.jpg by default
    img_file = os.path.join(save_path, "000001.jpg")
    return img_file if os.path.exists(img_file) else None