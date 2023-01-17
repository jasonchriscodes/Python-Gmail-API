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
    global msg
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is 
    # created automatically when the authorization flow completes for the first
    # time.y

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
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
    messages = results.get('messages', [])

    # if not labels:
    # message_count = int(input("How many messages do you want to see?"))
    if not messages:
     print("You have no new messages.")
    else:
    # for label in labels:
     message_count = 0
     for message in messages:
      msg = service.users().messages().get(userId='me', id=message['id']).execute()
      message_count = message_count + 1
     print("You have " + str(message_count) + " unread messages.")
     new_message_choice = input("Would you like to see your messages?").lower()
     if new_message_choice == "yes" or "y":
      email_data = msg['payload']['headers']
      for values in email_data:
       name = values["name"]
       if name == "From":
        from_name = values["value"]
        print("You have a new message from: " + from_name)
        print("     " + msg['snippet'][:50] + "...")
        print("\n")
      else:
        print("Good-bye.")


if __name__ == '__main__':
    main()
