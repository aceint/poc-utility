from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse
import os

app = FastAPI()

# Request model for video URL
class TranscriptRequest(BaseModel):
    url: str

def extract_video_id(url: str) -> str:
    """Extracts the video ID from a YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == 'youtu.be':
        return parsed_url.path[1:]  # Extract from shortened URL
    elif parsed_url.hostname in ['www.youtube.com', 'youtube.com']:
        query = parsed_url.query.split('v=')
        if len(query) > 1:
            return query[1].split('&')[0]  # Extract from full URL
    return None

def save_transcript_to_file(video_id: str, transcript: list) -> str:
    """Saves the transcript to a file."""
    file_name = f"transcript_{video_id}.txt"
    with open(file_name, 'w', encoding='utf-8') as f:
        for item in transcript:
            f.write(f"{item['start']:.2f}s: {item['text']}\n")
    return file_name

@app.post("/get_transcript")
async def get_transcript(request: TranscriptRequest):
    """Endpoint to fetch and save YouTube video transcript."""
    try:
        video_url = request.url
        if not video_url:
            raise HTTPException(status_code=400, detail="URL is required")

        video_id = extract_video_id(video_url)
        if not video_id:
            raise HTTPException(status_code=400, detail="Invalid YouTube URL")

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            file_name = save_transcript_to_file(video_id, transcript)
            return {"message": f"Transcript saved to {file_name}"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching transcript: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

