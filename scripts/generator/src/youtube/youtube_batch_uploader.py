import os
import json
import pickle
import sys
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# ensure project root is in path
PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

VIDEO_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
CLIENT_SECRET = os.path.join(PROJECT_ROOT, "scripts", "uploader", "auth", "client_secrets.json")
TOKEN_FILE = os.path.join(PROJECT_ROOT, "scripts", "uploader", "auth", "token.pickle")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def log(msg):
    # force lowercase for logs as per preference
    print("[" + datetime.now().strftime("%H:%M:%S") + "] " + msg.lower())

def get_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as f:
            creds = pickle.load(f)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
        with open(TOKEN_FILE, "wb") as f:
            pickle.dump(creds, f)

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, video_path, metadata):
    # extract metadata with lowercase fallback
    title = metadata.get("title", "chess puzzle").lower()
    description = metadata.get("description", "").lower() + "\n\ntune with us for more."
    tags = metadata.get("hashtags", ["chess", "shorts"])

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "24" # entertainment
        },
        "status": {
            "privacyStatus": "private" # default to private as requested
        }
    }

    media = MediaFileUpload(video_path, resumable=True, chunksize=-1)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            log("upload progress " + str(int(status.progress() * 100)) + "%")

    return response

def run_upload_pipeline():
    log("starting uploader")

    if not os.path.exists(VIDEO_DIR):
        log("video directory missing")
        return

    try:
        youtube = get_service()
    except Exception as e:
        log("authentication error: " + str(e))
        return

    videos = [v for v in os.listdir(VIDEO_DIR) if v.endswith(".mp4")]

    if not videos:
        log("no videos found")
        return

    for video in videos:
        name = os.path.splitext(video)[0]
        video_path = os.path.join(VIDEO_DIR, video)
        json_path = os.path.join(VIDEO_DIR, name + ".json")

        if not os.path.exists(json_path):
            log("skipping " + name + " (json missing)")
            continue

        with open(json_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        # check for 'youtube_metadata' key first, then fallback to root json
        metadata = raw.get("youtube_metadata", raw)

        log("uploading " + name)

        try:
            resp = upload_video(youtube, video_path, metadata)
            if resp and "id" in resp:
                log("uploaded successfully: " + resp["id"])
                
                # cleanup after successful upload
                os.remove(video_path)
                os.remove(json_path)
                log("artifacts cleaned for " + name)

        except Exception as e:
            log("upload error for " + name + ": " + str(e))

    log("uploader finished")

if __name__ == "__main__":
    run_upload_pipeline()