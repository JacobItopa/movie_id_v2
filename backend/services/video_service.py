import os
import yt_dlp
import uuid
import urllib.request

async def download_video(url: str) -> str:
    """
    Downloads the high-quality thumbnail of the video instead of the full video.
    This completely bypasses proxy streaming errors, timeouts, and Gemini parsing failures!
    Returns the path to the downloaded image file.
    """
    scraperapi_key = os.getenv("SCRAPER_API_KEY")
    if not scraperapi_key:
        raise ValueError("SCRAPER_API_KEY is missing")

    proxy_url = f"http://scraperapi:{scraperapi_key}@proxy-server.scraperapi.com:8001"
    
    ydl_opts = {
        'proxy': proxy_url,
        'extractor_args': {'youtube': ['player_client=android,ios']},
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True, 
    }

    print(f"Extracting metadata for {url}...")
    try:
         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            thumbnail_url = info_dict.get('thumbnail')
            
            if not thumbnail_url:
                print("No thumbnail found.")
                return None
                
            # Download the thumbnail image
            output_filename = f"temp_image_{uuid.uuid4().hex}.jpg"
            output_path = os.path.join(os.path.dirname(__file__), "..", output_filename)
            output_path = os.path.abspath(output_path)
            
            print(f"Downloading thumbnail from {thumbnail_url}...")
            # We don't need a proxy to download the thumbnail image from YouTube's CDN
            urllib.request.urlretrieve(thumbnail_url, output_path)
            
            if os.path.exists(output_path):
                return output_path
            return None
    except Exception as e:
        print(f"Error fetching thumbnail: {e}")
        return None
