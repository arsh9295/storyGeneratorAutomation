import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

# Scopes required for uploading video
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video(video_file_path, title, description, category_id="22", privacy_status="private"):
    # Load OAuth 2.0 credentials
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"  # Download this from Google Developers Console

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, SCOPES
    )
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )

    # Request body for video metadata
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": category_id  # 22 = People & Blogs
        },
        "status": {
            "privacyStatus": privacy_status  # "private", "public", or "unlisted"
        }
    }

    media_file = MediaFileUpload(video_file_path, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    print("Uploading video...")
    response = request.execute()
    print("Upload complete!")
    print(f"Video ID: {response['id']}")
    print(f"https://www.youtube.com/watch?v={response['id']}")

# Example usage
if __name__ == "__main__":
    upload_video(
        video_file_path="your_video.mp4",
        title="Test Video Upload",
        description="This is an automated upload using Python.",
        privacy_status="unlisted"  # Change to "public" when ready
    )
