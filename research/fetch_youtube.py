import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

API_KEY = "AIzaSyCpG_ihsw62jHxpd1KYWJVdV7V0S1h5fR0"

CHANNELS = {
    "nathan-gotch": "UCNEsahyXxNJvYNsMhru-UzQ",
    "vasco-seo": "UC99hX2gAnyK7asCu6Vhi0vg",
    "edward-sturm": "UCDxhBSgPvrFvyXLdpmygDhg",
    "matt-diggity": "UCP5A5lVxaT7cO_LehpxjTZg"
}

youtube = build("youtube", "v3", developerKey=API_KEY)

def get_recent_videos(channel_id, max_results=5):
    res = youtube.search().list(
        channelId=channel_id,
        part="snippet",
        order="date",
        maxResults=max_results,
        type="video"
    ).execute()
    videos = []
    for item in res.get("items", []):
        videos.append({
            "id": item["id"]["videoId"],
            "title": item["snippet"]["title"],
            "date": item["snippet"]["publishedAt"][:10]
        })
    return videos

def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join([t["text"] for t in transcript])
    except Exception as e:
        return f"Transcript unavailable: {str(e)}"

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "youtube-transcripts")

for name, channel_id in CHANNELS.items():
    print(f"\nFetching videos for {name}...")
    videos = get_recent_videos(channel_id)
    folder = os.path.join(output_dir, name)
    os.makedirs(folder, exist_ok=True)
    for video in videos:
        print(f"  Getting transcript: {video['title']}")
        transcript = get_transcript(video["id"])
        filename = f"{video['date']}_{video['id']}.txt"
        filepath = os.path.join(folder, filename)
        with open(filepath, "w") as f:
            f.write(f"Title: {video['title']}\n")
            f.write(f"Date: {video['date']}\n")
            f.write(f"URL: https://youtube.com/watch?v={video['id']}\n\n")
            f.write(transcript)
        print(f"  Saved: {filename}")

print("\nDone!")
