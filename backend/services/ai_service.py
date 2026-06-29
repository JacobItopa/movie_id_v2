import os
import json
import time
import mimetypes
import google.generativeai as genai

async def identify_movie(video_path: str) -> dict:
    """
    Uploads a video to Gemini and asks it to identify the movie/TV show.
    Returns a dictionary with 'title' and 'year'.
    """
    gemini_key = os.getenv("GOOGLE_API_KEY")
    if not gemini_key:
        raise ValueError("GOOGLE_API_KEY is missing")

    genai.configure(api_key=gemini_key)
    
    # Dynamically determine the mime type so Gemini doesn't reject it as a generic binary file
    mime_type, _ = mimetypes.guess_type(video_path)
    if not mime_type:
        mime_type = "video/mp4" # fallback
        
    file_size = os.path.getsize(video_path)
    print(f"Uploading {video_path} (Size: {file_size} bytes, MimeType: {mime_type}) to Gemini...")
    video_file = genai.upload_file(path=video_path, mime_type=mime_type)
    
    print(f"Completed upload: {video_file.uri}")
    
    # Wait for the file to be processed by Gemini
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = genai.get_file(video_file.name)
        
    if video_file.state.name == "FAILED":
        raise ValueError("Gemini failed to process the video.")
        
    print("Video processed. Querying model...")

    prompt = (
        "Watch this short video clip. Your task is to identify the movie or TV show it is from. "
        "Return ONLY a JSON object with two keys: 'title' (the name of the movie/show) and 'year' (the release year). "
        "Do not include any markdown formatting like ```json or any other text. Just the raw JSON object."
    )
    
    # Use Gemini 2.5 Flash which is fast and supports video
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    
    response = model.generate_content([video_file, prompt],
                                      generation_config={"temperature": 0.0})
                                      
    try:
        # Cleanup the uploaded file to save space on Google's servers
        genai.delete_file(video_file.name)
        
        result_text = response.text.strip()
        # Clean up possible markdown tags if Gemini ignores the prompt
        if result_text.startswith("```json"):
             result_text = result_text.replace("```json", "").replace("```", "").strip()
        
        movie_info = json.loads(result_text)
        print(f"Identified Movie: {movie_info}")
        return movie_info
    except json.JSONDecodeError as e:
        print(f"Failed to parse Gemini response: {response.text}")
        return None
