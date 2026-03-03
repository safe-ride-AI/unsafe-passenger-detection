import yt_dlp
import os

CHANNEL_URL = "https://www.youtube.com/@ShakargarhFlyers/shorts"
OUTPUT_DIR = "downloads-ShakargarhFlyers"
os.makedirs(OUTPUT_DIR, exist_ok=True)

COOKIES = "cookies.txt"
USE_COOKIES = os.path.exists(COOKIES)


def extract_all_video_ids(channel_url):
    print("\n🔍 Fetching all video IDs...")

    ydl_opts = {
        "extract_flat": True,
        "quiet": True,
        "dump_single_json": True,

        # 🔥 FIX: bypass sign-in checks
        "extractor_args": {
            "youtube": {"player_client": ["android"]}
        }
    }

    if USE_COOKIES:
        ydl_opts["cookies"] = COOKIES

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)

    video_ids = []

    if "entries" in info:
        for entry in info["entries"]:
            if entry and "id" in entry:
                video_ids.append(entry["id"])

    print(f"📌 Found {len(video_ids)} videos")
    return video_ids


def download_video(video_id, index):
    url = f"https://www.youtube.com/watch?v={video_id}"
    print(f"\n⬇ Downloading {index}: {url}")

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": f"{OUTPUT_DIR}/%(title)s_{video_id}.%(ext)s",
        "merge_output_format": "mp4",

        # 🔥 FIX: use android API → no login required
        "extractor_args": {
            "youtube": {"player_client": ["android"]}
        }
    }

    if USE_COOKIES:
        ydl_opts["cookies"] = COOKIES

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✔ Done")
    except Exception as e:
        print(f"❌ Error downloading {video_id}: {e}")


if __name__ == "__main__":
    print("""
===============================================
📺 YOUTUBE CHANNEL VIDEO DOWNLOADER
===============================================
    """)

    ids = extract_all_video_ids(CHANNEL_URL)

    for i, vid in enumerate(ids, 1):
        download_video(vid, i)

    print("\n🎉 ALL DONE!")
    print(f"📂 Saved in folder: {OUTPUT_DIR}")
