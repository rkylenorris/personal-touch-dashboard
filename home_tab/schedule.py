from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime


def get_calendar_events(credentials_file: str, calendar_id: str, max_results: int = 10) -> list:
    """
    Fetches calendar events from Google Calendar API.

    Args:
        credentials_file (str): Path to the service account credentials JSON file.
        calendar_id (str): The ID of the calendar to fetch events from.
        max_results (int): Maximum number of events to return.
    Returns:
        list: A list of calendar events.
    """
    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(
        credentials_file,
        scopes=["https://www.googleapis.com/auth/calendar.readonly"]
    )

    # Build the Google Calendar API service
    service = build("calendar", "v3", credentials=credentials)

    # Get the current time in RFC3339 format
    # now = datetime.datetime.now(datetime.UTC).isoformat()
    
    import pytz

    eastern = pytz.timezone("America/New_York")
    now = datetime.datetime.now(eastern).isoformat()


    # Fetch events from the calendar
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])




if __name__ == "__main__":
    # Example usage
    CREDENTIALS_FILE = r"keys\dashboard-calendar.json"
    CALENDAR_ID = "rodermus@gmail.com"  # Use "primary" for the primary calendar
    MAX_RESULTS = 10
    
    events = get_calendar_events(CREDENTIALS_FILE, CALENDAR_ID, MAX_RESULTS)
    with open("calendar_events.json", "w") as f:
        import json
        json.dump(events, f, indent=4)
    
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(f"{start}: {event['summary']}")