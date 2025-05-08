import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
from django.conf import settings  # Important!

# Get OAuth access token
def get_zoom_access_token():
    url = "https://zoom.us/oauth/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {
        "grant_type": "account_credentials",
        "account_id": settings.ZOOM_ACCOUNT_ID
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            auth=HTTPBasicAuth(settings.ZOOM_CLIENT_ID, settings.ZOOM_CLIENT_SECRET)
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.HTTPError as e:
        print("Zoom token error response:", response.text)
        return {'error': f'Zoom token error: {response.text}'}
    except requests.exceptions.RequestException as e:
        print("Zoom token error:", str(e))
        return {'error': str(e)}

# Create Zoom meeting
def create_zoom_meeting(topic, duration, start_time_str):
    try:
        token = get_zoom_access_token()
        if isinstance(token, dict) and 'error' in token:
            return token  # return the token error if getting it failed

        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

        payload = {
            'topic': topic,
            'type': 2,
            'start_time': start_time_str,
            'duration': duration,
            'timezone': 'UTC',
            'settings': {
                'host_video': True,
                'participant_video': True,
                'join_before_host': False,
                'mute_upon_entry': True,
                'auto_recording': 'cloud',
                'waiting_room': True
            }
        }

        response = requests.post(
            'https://api.zoom.us/v2/users/me/meetings',
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Zoom API error: {e}")
        return {'error': str(e)}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {'error': str(e)}
