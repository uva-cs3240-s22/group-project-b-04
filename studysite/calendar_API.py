from decouple import config
from google.oauth2 import service_account
from  google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import googleapiclient.discovery
import datetime
# from Google import Create_Service
# from pprint import pprint
import os.path

#CAL_ID = 'mv5vc@virginia.edu'
SCOPES = ['https://www.googleapis.com/auth/calendar']
#SERVICE_ACCOUNT_FILE = './google-credentials.json'



def test_calendar():
    print("RUNNING TEST_CALENDAR()")

    # print(dir(service))
    # credentials = None
    # # The file token.json stores the user's access and refresh tokens, and is
    # # created automatically when the authorization flow completes for the first
    # # time.
    # if os.path.exists('token.json'):
    #     credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    # # If there are no (valid) credentials available, let the user log in.
    # if not credentials or not credentials.valid:
    #     if credentials and credentials.expired and credentials.refresh_token:
    #         credentials.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file(
    #             'credentials.json', SCOPES)
    #         credentials = flow.run_local_server(port=0)
    #     # Save the credentials for the next run
    #     with open('token.json', 'w') as token:
    #         token.write(credentials.to_json())
    #credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    #https://www.programcreek.com/python/example/124838/google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file
    # credentials = None
    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    #         credentials = pickle.load(token)
    # if not credentials or not credentials.valid:
    #     if credentials and credentials.expired and credentials.refresh_token:
    #         credentials.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_secrets_file('google-credentials.json', scopes=SCOPES)
    #         credentials = flow.run_console(port=0)
    # with open('token.pickle', 'wb') as token:
    #     pickle.dump(creds, token)
    creds = None

    # flow = InstalledAppFlow.from_client_secrets_file('google-credentials.json', SCOPES)
    # creds = flow.run_local_server(port=8000)

    if os.path.exists('token2.json'):
         creds = Credentials.from_authorized_user_file('token2.json', SCOPES)
     # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'google-credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())
    CLIENT_SECRET_FILE = 'google-credentials.json'
    service = Create_Service(CLIENT_SECRET_FILE, 'calendar', 'v3', SCOPES)
    #flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file('google-credentials.json', SCOPES)
    #flow.redirect_uri = 'http://127.0.0.1:8000/studysite/accounts/google/login/callback/'
   # service = googleapiclient.discovery.build('calendar', 'v3', credentials=creds)

    result = service.calendarList().list().execute()
    CAL_ID = result['items'][0]['id']
    #result = service.events().list(calendarId=calendar_id).execute()

    # CREATE A NEW EVENT
    event = {
    'summary': "Ben Hammond Tech's Super Awesome Event",
    'location': 'Denver, CO USA',
    'description': 'https://benhammond.tech',
    'start': {
        'date': f"{datetime.date.today()}",
        'timeZone': 'America/New_York',
    },
    'end': {
        'date': f"{datetime.date.today() + datetime.timedelta(days=1)}",
        'timeZone': 'America/New_York',
    },
    }
    event = service.events().insert(calendarId=CAL_ID, body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))
    # service.events().insert(calendarId=CAL_ID, body=new_event).execute()
    # print('Event created')

 # GET ALL EXISTING EVENTS
    events_result = service.events().list(calendarId=CAL_ID, maxResults=2500).execute()
    events = events_result.get('items', [])



    # LOG THEM ALL OUT IN DEV TOOLS CONSOLE
    for e in events:

        print(e)

    #uncomment the following lines to delete each existing item in the calendar
    #event_id = e['id']
        # service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()


    return events
