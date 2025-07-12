import os
import datetime
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from config.settings import SCOPES

# Load environment variables
load_dotenv()

def fetch_calendar():
    creds = None

    # Build client config from .env
    client_config = {
        "installed": {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "project_id": os.getenv("GOOGLE_PROJECT_ID"),
            "auth_uri": os.getenv("GOOGLE_AUTH_URI"),
            "token_uri": os.getenv("GOOGLE_TOKEN_URI"),
            "auth_provider_x509_cert_url": os.getenv("GOOGLE_AUTH_PROVIDER_X509_CERT_URL"),
            "client_secret": os.getenv("GOOGLE_CLIENT_SECRET"),
            "redirect_uris": [os.getenv("GOOGLE_REDIRECT_URI")]
        }
    }

    # Define the correct relative path to the token file
    TOKEN_DIR = "api_clients"
    TOKEN_PATH = os.path.join(TOKEN_DIR, "token.json")

    # Ensure the directory exists
    os.makedirs(TOKEN_DIR, exist_ok=True)

    # Check if the token file exists
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        print("Using existing credentials from token.json")
    else:
        print("No existing credentials found, initiating OAuth flow...")
        flow = InstalledAppFlow.from_client_config(client_config, SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the new token
    with open(TOKEN_PATH, "w") as token:
        token.write(creds.to_json())
        print("token.json saved")

    service = build("calendar", "v3", credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=5,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    event_list = []
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        event_list.append({
            "start": start,
            "summary": event.get("summary", "No title")
        })

    return {
        "meeting": bool(event_list),
        "events": event_list
    }
