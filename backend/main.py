import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from services.video_service import download_video
from services.ai_service import identify_movie
from services.search_service import search_movie_links

load_dotenv()

app = FastAPI(title="Movie ID API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for MVP
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url: str

class MovieResponse(BaseModel):
    title: str
    year: str
    streaming_links: list[dict]
    error: str | None = None

@app.post("/api/identify-movie", response_model=MovieResponse)
async def identify_movie_endpoint(request: URLRequest):
    video_path = None
    try:
        # 1. Download Video using yt-dlp via ZenRows
        video_path = await download_video(request.url)
        if not video_path:
            raise HTTPException(status_code=500, detail="Failed to download video")

        # 2. Identify Movie using Gemini
        movie_info = await identify_movie(video_path)
        if not movie_info or not movie_info.get("title"):
             raise HTTPException(status_code=500, detail="Could not identify the movie")

        title = movie_info["title"]
        year = str(movie_info.get("year", ""))

        # 3. Search for streaming links using Tavily
        search_results = await search_movie_links(title, year)

        return MovieResponse(
            title=title,
            year=year,
            streaming_links=search_results
        )
    except Exception as e:
        print(f"Error processing request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cleanup video file
        if video_path and os.path.exists(video_path):
            try:
                os.remove(video_path)
            except Exception as e:
                print(f"Error cleaning up video: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
