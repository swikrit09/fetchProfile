import os
import json 
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv



load_dotenv()

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
def  youtube_authenticate():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "./utils/client_secret_235434982429-sf20gq52rcqm7vc9bci6uhtr0q8906hk.apps.googleusercontent.com.json"
    print(client_secrets_file)
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes
        )
    credentials = flow.run_local_server(port=4000)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)
    request = youtube.channels().list(
        part="contentDetails",
        mine=True
    )
    response = request.execute()

    print(response)
    return response

