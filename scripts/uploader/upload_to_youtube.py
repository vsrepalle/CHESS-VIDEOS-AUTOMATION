import os
import sys
import pickle
import json
import argparse
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CLIENT_SECRETS_FILE = r"C:\VISWA\CHESS_PRO_AUTOMATION\client_secret.json"
TOKEN_PICKLE = r"C:\VISWA\CHESS_PRO_AUTOMATION\token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token: creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(port=0, prompt='select_account')
        with open(TOKEN_PICKLE, 'wb') as token: pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)

def upload_video(video_path, json_path=None):
    if not os.path.exists(video_path): return False
    
    # Defaults
    title = f"Chess News: {os.path.basename(video_path)}"
    desc = "Daily Chess Updates. Tune with us for more!"
    
    # Load Gemini Metadata
    if json_path and os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            title = data.get('tournament_name', title)[:100]
            desc = f"{data.get('details', '')}\n\n{data.get('hook_text', '')}\n\nTune with us for more!"

    try:
        youtube = get_authenticated_service()
        body = {
            "snippet": {"title": title, "description": desc, "tags": ["chess", "shorts"], "categoryId": "22"},
            "status": {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
        }
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        print(f"✅ Video ID: {response.get('id')}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video")
    parser.add_argument("--metadata")
    args = parser.parse_args()
    success = upload_video(args.video, args.metadata)
    sys.exit(0 if success else 1)