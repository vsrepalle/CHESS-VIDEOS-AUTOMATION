import os
import json
import shutil
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# ------------------------------------------------
# CONFIGURATION
# ------------------------------------------------

PROJECT_ROOT = r"C:\VISWA\CHESS_PRO_AUTOMATION"

VIDEO_DIR = os.path.join(PROJECT_ROOT, "output", "videos")
HISTORY_DIR = os.path.join(PROJECT_ROOT, "dump_zone", "processed_history")

CLIENT_SECRET = os.path.join(PROJECT_ROOT, "client_secret.json")
TOKEN_FILE = os.path.join(PROJECT_ROOT, "youtube_token.pickle")

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


# ------------------------------------------------
# LOGGER
# ------------------------------------------------

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ------------------------------------------------
# AUTHENTICATION
# ------------------------------------------------

def get_youtube_service():

    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


# ------------------------------------------------
# CLEANUP
# ------------------------------------------------

def purge_project(project_name):

    log(f"🧹 Starting cleanup for: {project_name}")

    for ext in [".mp4", ".json"]:
        file_path = os.path.join(VIDEO_DIR, f"{project_name}{ext}")

        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                log(f"  - Deleted artifact: {project_name}{ext}")
            except Exception as e:
                log(f"  - ⚠️ Could not delete artifact: {e}")

    source_folder = os.path.join(HISTORY_DIR, project_name)

    if os.path.exists(source_folder):
        try:
            shutil.rmtree(source_folder)
            log(f"  - Deleted source folder: {project_name}")
        except Exception as e:
            log(f"  - ⚠️ Could not delete source folder: {e}")

    log(f"✅ Cleanup complete for {project_name}")


# ------------------------------------------------
# ACTUAL UPLOAD FUNCTION
# ------------------------------------------------

def upload_video(youtube, video_path, metadata):

    body = {
        "snippet": {
            "title": metadata.get("title", "Chess Puzzle"),
            "description": metadata.get("description", ""),
            "tags": metadata.get("tags", []),
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": metadata.get("privacyStatus", "public")
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=-1,
        resumable=True
    )

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = None

    while response is None:
        status, response = request.next_chunk()

        if status:
            log(f"⬆ Upload progress: {int(status.progress() * 100)}%")

    return response


# ------------------------------------------------
# MAIN BATCH PROCESS
# ------------------------------------------------

def run_uploader():

    log("🚀 Initializing Batch Uploader...")

    if not os.path.exists(VIDEO_DIR):
        log("❌ Error: Video directory not found")
        return

    youtube = get_youtube_service()

    videos = [f for f in os.listdir(VIDEO_DIR) if f.lower().endswith(".mp4")]

    if not videos:
        log("⚠️ No videos found in output\\videos to upload")
        return

    for video_file in videos:

        project_name = os.path.splitext(video_file)[0]

        json_file = os.path.join(VIDEO_DIR, f"{project_name}.json")
        video_path = os.path.join(VIDEO_DIR, video_file)

        if not os.path.exists(json_file):
            log(f"❌ Skipping {project_name}: JSON missing")
            continue

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except Exception as e:
            log(f"❌ Metadata error for {project_name}: {e}")
            continue

        log(f"📤 Uploading: {project_name} to YouTube...")

        try:

            response = upload_video(youtube, video_path, metadata)

            if response and "id" in response:

                log(f"🌟 Successfully uploaded {project_name}!")
                log(f"📺 Video ID: {response['id']}")

                purge_project(project_name)

            else:

                log(f"❌ Upload failed for {project_name}")

        except Exception as e:

            log(f"❌ Upload exception for {project_name}: {e}")

    log("🏁 All upload tasks finished")


# ------------------------------------------------

if __name__ == "__main__":
    run_uploader()