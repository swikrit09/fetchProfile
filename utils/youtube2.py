from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from dotenv import load_dotenv
import os


load_dotenv()
# Replace these with your OAuth 2.0 credentials
def auth_user():
    CLIENT_ID = os.getenv('YT_CLIENT_ID')
    CLIENT_SECRET = os.getenv('YT_CLIENT_SECRET')
    REDIRECT_URI =os.getenv('YT_REDIRECT_URI')
    SCOPE = 'https://www.googleapis.com/auth/youtube.readonly'

    flow = OAuth2WebServerFlow(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri='http://localhost:5000/oauth2callback')
    # This will provide the URL to which the user must go to grant access
    auth_uri = flow.step1_get_authorize_url()
    print(auth_uri)

    # After authorization, Google redirects back to your app with a code in the URL.
    # You should extract this code and use it to request an access token.
    code = 'RECEIVED_AUTHORIZATION_CODE'
    credentials = flow.step2_exchange(code)

    youtube = build('youtube', 'v3', credentials=credentials)

    # Retrieve the user's uploads playlist ID
    channels_response = youtube.channels().list(mine=True, part='contentDetails').execute()
    for channel in channels_response['items']:
        uploads_list_id = channel['contentDetails']['relatedPlaylists']['uploads']

        # Retrieve the videos in the uploads playlist
        playlistitems_list_request = youtube.playlistItems().list(
            playlistId=uploads_list_id,
            part='snippet',
            maxResults=50
        )

        while playlistitems_list_request:
            playlistitems_list_response = playlistitems_list_request.execute()

            for playlist_item in playlistitems_list_response['items']:
                title = playlist_item['snippet']['title']
                video_id = playlist_item['snippet']['resourceId']['videoId']
                print(f'{title} (https://www.youtube.com/watch?v={video_id})')

            playlistitems_list_request = youtube.playlistItems().list_next(
                playlistitems_list_request, playlistitems_list_response)