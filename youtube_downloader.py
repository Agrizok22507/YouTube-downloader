import random
import os
import subprocess
import shutil

bad_symbols = [":", "/", "\\", "*", "?", '"', "<", ">", "|"]

def save_video(url, path, quality, video_format):
    command = f"""yt-dlp -f "bv[height<={quality}][ext={video_format}]+ba[ext=m4a]/b[ext={video_format}]" \
        --sleep-requests {random.uniform(1.5, 3.5)} \
        --min-sleep-interval 5 \
        --max-sleep-interval 15 \
        --embed-metadata \
        --embed-thumbnail \
        --write-description \
        --no-write-auto-subs \
        --downloader aria2c \
        --download-archive archive.txt \
        --restrict-filenames \
        --downloader-args "aria2c:-x 8 -s 8 -j 1" \
        -o "{path}/%(title)s.%(ext)s" \
        "{url}" """
    
    os.system(command)

def search_videos(search_query, count):
    urls = []
    command = ["yt-dlp", f"ytsearch{count}:{search_query}", "--get-id", "--flat-playlist"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        for video_id in result.stdout.strip().split('\n'):
            if video_id:
                urls.append(f"https://youtube.com/watch?v={video_id}")
    except subprocess.CalledProcessError as e:
        print(f"🚫 Error with searching: {e}")
    return urls

def is_ytdlp_installed():
    return shutil.which("yt-dlp") is not None

def check_for_bad_symbols(text):
    for symbol in text:
        if symbol in bad_symbols:
            return symbol
    return True

def main():
    if not is_ytdlp_installed():
        print("🚫 Error: yt-dlp not installed or not added to PATH!")
        print("📥 Install it by: pip3 install yt-dlp")
        return

    print("🥔 YouTube Downloader")
    home_folder = input("📁 Your home folder (like /home/user or C:/Users/Name): ")
    save_folder = input("📁 Your folder for save (like /Downloads/Videos): ")
    
    base_path = os.path.join(home_folder.strip(), save_folder.strip('/').strip('\\'))

    # search = input("🔍 Your request for search (split by ','): ")
    with open("requests.txt", "r", encoding="utf-8") as f:
        search = f.read()
    count_videos_from_request = int(input("Count videos from one search request: "))
    quality = int(input("💻 Quality of saving videos (like '1080'): "))
    video_format = input("⚙️ Video format (like 'mp4'): ")

    search_requests = [req.strip() for req in search.split(",")]

    count_all_videos = count_videos_from_request * len(search_requests)
    count_all_requests = len(search_requests)
    
    saved_videos = 0
    saved_requests = 0

    check = check_for_bad_symbols(search)

    if check is not True:
        print(f"🚫 Error: in search requests bad symbol '{check}'")
        return

    if not os.path.isdir(base_path):
        os.makedirs(base_path)

    print("\n⏳ Starting...")

    for search_request in search_requests:
        try:
            request_folder = os.path.join(base_path, search_request)
            if not os.path.isdir(request_folder):
                os.mkdir(request_folder)
            
            print(f"\n🔍 Searching by '{search_request}'...")
            video_urls = search_videos(search_request, count_videos_from_request)
            
            print(f"🔍 Searched urls: {video_urls}")
            for video_url in video_urls:
                print(f"📂 Saving '{video_url}'")
                save_video(video_url, request_folder, quality, video_format)
                print(f"✅ Video {video_url} saved")
                saved_videos += 1
                print(f"✅ Saved {saved_videos}/{count_all_videos} videos")
            
            saved_requests += 1
            print(f"\n✅ Requests completed: {saved_requests}/{count_all_requests}\n")
        
        except Exception as e:
            print(f"🚫 Error with saving '{search_request}': {e}")

    print("\n\n✅ Videos successfully saved!")
    print("Saved:")
    print(f"Requests: {saved_requests}/{count_all_requests}")
    print(f"Videos: {saved_videos}/{count_all_videos}")
    print(f"Videos saved to {base_path}")

if __name__ == '__main__':
    main()
