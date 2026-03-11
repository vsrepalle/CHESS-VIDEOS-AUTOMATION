import os
import sys
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Explicit paths
CLIENT_SECRETS_FILE = r"C:\VISWA\CHESS_PRO_AUTOMATION\client_secret.json"
TOKEN_PICKLE = r"C:\VISWA\CHESS_PRO_AUTOMATION\token.pickle"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload", "https://www.googleapis.com/auth/youtube.readonly"]

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as token:
            creds = pickle.load(token)
            
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            # DEBUGGER 1: Force account selection to see Brand Accounts
            creds = flow.run_local_server(port=0, prompt='select_account')
        with open(TOKEN_PICKLE, 'wb') as token:
            pickle.dump(creds, token)

    service = build("youtube", "v3", credentials=creds)

    # DEBUGGER 2: Identify the channel BEFORE uploading
    try:
        ch_request = service.channels().list(mine=True, part="snippet,id").execute()
        if 'items' in ch_request:
            channel = ch_request['items'][0]
            print("\n" + "="*50)
            print(f"📡 TARGET CHANNEL NAME: {channel['snippet']['title']}")
            print(f"🆔 TARGET CHANNEL ID:   {channel['id']}")
            print("="*50 + "\n")
        else:
            print("❌ ERROR: No channel found for this account!")
    except Exception as e:
        print(f"❌ DEBUGGER FAILED: Could not fetch channel info. {e}")
    
    return service

def upload_video(video_path):
    if not os.path.exists(video_path):
        print(f"❌ Error: File not found: {video_path}")
        return

    youtube = get_authenticated_service()
    
    body = {
        "snippet": {
            "title": f"Chess Shorts: {os.path.basename(video_path)}",
            "description": "Daily Chess Updates. Tune with us for more!",
            "tags": ["chess", "shorts"],
            "categoryId": "22" 
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    print(f"☁️ Uploading {os.path.basename(video_path)}...")
    try:
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        # DEBUGGER 3: Confirm Video ID and Final Channel
        print(f"✅ UPLOAD SUCCESSFUL!")
        print(f"📹 Video ID: {response.get('id')}")
        print(f"🔗 Verification Link: https://www.youtube.com/watch?v={response.get('id')}")
    except Exception as e:
        print(f"❌ UPLOAD FAILED: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        upload_video(sys.argv[1])
    else:
        print("❌ Error: No video path provided.")