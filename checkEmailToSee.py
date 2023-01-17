from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import time
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is 
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
     with open('token.pickle', 'rb') as token:
      creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
     if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
     else:
      flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
      # Save the credentials for the next run 
      with open('token.pickle', 'wb') as token:
       pickle.dump(creds,token)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    # results = service.users().labels().list(userId='me').execute()
    # labels = results.get('labels', [])

    # Get Messages
    results = service.users().messages().list(userId='me', labelIds=['INBOX']).execute()
    messages = results.get('messages', [])

    # if not labels:
    message_count = int(input("How many messages do you want to see?"))
    if not messages:
     print("No messages found.")
    else:
     print("Messages:") 
    # for label in labels:
    for message in messages[:message_count]:
     msg = service.users().messages().get(userId='me', i6
     d=message['id']).execute()
     print(msg['snippet'])
     print("\n")
     time.sleep(2)
     # print(label['name'])


if __name__ == '__main__':
    main()