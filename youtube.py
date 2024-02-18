from googleapiclient.discovery import build
import re

# Your API key
API_KEY = "AIzaSyCFMYRpYP5EL9IGectX4vFj39pZBChN91E"

# Function to extract channel ID from a video URL
def extract_channel_id(video_url):
    video_id_match = re.search(r'(?:https?://)?(?:www\.)?(?:youtube\.com/.*v=|youtu\.be/)([^&\n?#]+)', video_url)
    if video_id_match:
        video_id = video_id_match.group(1)
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        response = youtube.videos().list(part='snippet', id=video_id).execute()
        if 'items' in response:
            return response['items'][0]['snippet']['channelId']
    return None

# Function to get channel information using channel ID
def get_channel_info(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    response = youtube.channels().list(part='snippet', id=channel_id).execute()
    if 'items' in response:
        return response['items'][0]['snippet']
    return None

# Example usage
video_url = "https://www.youtube.com/watch?v=ZEquIbjuZGs&t=6s&ab_channel=Sau"
channel_id = extract_channel_id(video_url)
if channel_id:
    channel_info = get_channel_info(channel_id)
    if channel_info:
        print("Channel Name:", channel_info['title'])
        print("Channel Description:", channel_info['description'])
    else:
        print("Channel not found.")
else:
    print("Invalid YouTube video URL.")
