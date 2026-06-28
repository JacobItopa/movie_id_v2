import os
import yt_dlp
import uuid

async def download_video(url: str) -> str:
    """
    Downloads a video from YouTube using yt-dlp through the ZenRows proxy.
    Returns the path to the downloaded video file.
    """
    zenrows_key = os.getenv("ZENROWS_API_KEY")
    if not zenrows_key:
        raise ValueError("ZENROWS_API_KEY is missing")

    # Construct the ZenRows proxy URL using premium residential proxies
    proxy_url = f"http://{zenrows_key}&premium_proxy=true:@proxy.zenrows.com:8001"
    
    # Generate a unique filename for the download
    output_filename = f"temp_video_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(os.path.dirname(__file__), "..", output_filename)
    output_path = os.path.abspath(output_path)

    ydl_opts = {
        'format': 'best[ext=mp4]/best', # More robust format selection for Shorts
        'outtmpl': output_path,
        'proxy': proxy_url,
        'extractor_args': {'youtube': ['player_client=android,ios']},
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, 
    }

    print(f"Downloading video from {url}...")
    try:
         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
         if os.path.exists(output_path):
             return output_path
         else:
             print("Download completed but file not found.")
             return None
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None
