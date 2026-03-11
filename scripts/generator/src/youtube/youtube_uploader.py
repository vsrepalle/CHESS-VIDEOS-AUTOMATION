import os
import sys
import json
import pickle
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

# CONFIG
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRET_FILE = "client_secret.json"
TOKEN_FILE = "token.pickle"

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, json_path):
    youtube = get_authenticated_service()

    # FIX: Added encoding="utf-8" to prevent UnicodeDecodeError
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    
    # Check for nested or flat metadata
    meta = data.get('youtube_metadata', data)

    body = {
        "snippet": {
            "title": meta.get("title", "Chess Puzzle"),
            "description": meta.get("description", "Daily Chess Short"),
            "tags": meta.get("tags", ["chess", "shorts"]),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": meta.get("privacy", "private")
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    print(f"☁️ Uploading {os.path.basename(video_path)}...")
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Progress: {int(status.progress() * 100)}%")

    print(f"✅ Success! Video ID: {response['id']}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--json", required=True)
    args = parser.parse_args()
    
    upload_video(args.video, args.json)