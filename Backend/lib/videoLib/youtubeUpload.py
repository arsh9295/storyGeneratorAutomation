#!/usr/bin/env python3
import os
import sys
import time
import random
import httplib2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
import globalVariables as gv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from oauth2client.client import flow_from_clientsecrets

# Retry configuration
httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (
    IOError, httplib2.HttpLib2Error, httplib2.ServerNotFoundError
)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# OAuth2 client secrets file
CLIENT_SECRETS_FILE = gv.youtubeAuthConfigFile

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE = "youtube"
YOUTUBE_API_VERSION = "v3"

def get_authenticated_service():
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_UPLOAD_SCOPE)
    storage = Storage("yt_oauth2.json")
    credentials = storage.get()
    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage)
    return build(YOUTUBE_API_SERVICE, YOUTUBE_API_VERSION, credentials=credentials)

def set_thumbnail(youtube, video_id, thumbnail_path):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    )
    response = request.execute()
    print("Thumbnail uploaded!")


def resumable_upload(request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            status, response = request.next_chunk()
            if response and "id" in response:
                return response["id"]
            else:
                raise Exception("Upload failed: no video ID.")
        except HttpError as e:
            if e.resp.status not in RETRIABLE_STATUS_CODES:
                raise
            error = f"HTTP error {e.resp.status}"
        except RETRIABLE_EXCEPTIONS as e:
            error = f"Retryable error: {e}"
        retry += 1
        if retry > MAX_RETRIES:
            raise Exception("Exceeded maximum retries.")
        sleep = random.random() * (2 ** retry)
        print(f"{error}. Sleeping {sleep:.2f} seconds and retrying...")
        time.sleep(sleep)

def initializeUpload(file, title=None, description=None, category="24", privacyStatus="private", keywords=None):
    youtube = get_authenticated_service()
    tags = keywords.split(",") if keywords else None

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category
        },
        "status": {"privacyStatus": privacyStatus}
    }

    media = MediaFileUpload(file, chunksize=-1, resumable=True)
    insert_request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )
    video_id = resumable_upload(insert_request)
    print(f"Video uploaded! ID: {video_id}")

# if __name__ == "__main__":
#     argparser.add_argument("--file", required=True, help="Video file path")
#     argparser.add_argument("--title", help="Video title", default="Test Title")
#     argparser.add_argument("--description", help="Video description",
#                            default="Test Description")
#     argparser.add_argument("--category", default="22", help="Numeric category")
#     argparser.add_argument("--keywords", help="Comma-separated keywords",
#                            default="")
#     argparser.add_argument("--privacyStatus", choices=["public","private","unlisted"],
#                            default="private", help="Video privacy status")
#     args = argparser.parse_args()

#     if not os.path.exists(args.file):
#         print(f"ERROR: file '{args.file}' not found.")
#         sys.exit(1)

#     youtube = get_authenticated_service()
#     initializeUpload(youtube, args)
