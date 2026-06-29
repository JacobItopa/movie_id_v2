import os
import yt_dlp
import uuid

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
    
    # Generate a unique filename for the download
    output_filename = f"temp_video_{uuid.uuid4().hex}.mp4"
    output_path = os.path.join(os.path.dirname(__file__), "..", output_filename)
    output_path = os.path.abspath(output_path)

    ydl_opts = {
        'format': 'best[ext=mp4]/b/bestvideo/best', # Extremely robust fallback chain
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
