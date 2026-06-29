import os
import yt_dlp
import uuid
import imageio_ffmpeg

async def download_video(url: str) -> str:
    """
    Downloads a video from YouTube using yt-dlp through the ZenRows proxy.
    Returns the path to the downloaded video file.
    """
    scraperapi_key = os.getenv("SCRAPER_API_KEY")
    if not scraperapi_key:
        raise ValueError("SCRAPER_API_KEY is missing")

    # Construct the ScraperAPI proxy URL
    proxy_url = f"http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001"
    
    # Generate a unique filename template allowing yt-dlp to choose the correct extension
    output_filename_template = f"temp_video_{uuid.uuid4().hex}.%(ext)s"
    output_path_template = os.path.join(os.path.dirname(__file__), "..", output_filename_template)
    output_path_template = os.path.abspath(output_path_template)

    ydl_opts = {
        'format': '18/best[ext=mp4]/b', # 18 is the golden standard 360p pre-merged MP4 format that never requires ffmpeg
        'outtmpl': output_path_template,
        'proxy': proxy_url,
        'extractor_args': {'youtube': ['player_client=android,ios']},
        'socket_timeout': 60,
        'retries': 10,
        'fragment_retries': 10,
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, 
    }

    print(f"Downloading video from {url}...")
    try:
         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            downloaded_file_path = ydl.prepare_filename(info_dict)
            
         if os.path.exists(downloaded_file_path):
             return downloaded_file_path
         else:
             print("Download completed but file not found.")
             return None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
