from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from typing import Union
from bot import settings


class GoogleSheets:
    # If modifying these scopes, delete the file token.json.
    SCOPES = settings.SCOPES

    # The ID and range of a sample spreadsheet.
    SAMPLE_SPREADSHEET_ID = settings.SAMPLE_SPREADSHEET_ID

    def __init__(self):
        """

        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('C:\\Users\\mrkim\\PycharmProjects\\pythonProject2\\GoogleSheets\\token.json'):
            creds = Credentials.from_authorized_user_file('C:\\Users\\mrkim\\PycharmProjects\\pythonProject2\\GoogleSheets\\token.json', GoogleSheets.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'C:\\Users\\mrkim\\PycharmProjects\\pythonProject2\\GoogleSheets\\credentials.json',
                    GoogleSheets.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('C:\\Users\\mrkim\\PycharmProjects\\pythonProject2\\GoogleSheets\\token.json', 'w') as token:
                token.write(creds.to_json())

        try:
            self.service = build('sheets', 'v4', credentials=creds)
        except HttpError as err:
            print(err)

    def batch_get_values(self, spreadsheet_id: str = None,
                         _range_names: Union[str, list[str]] = 'A1') -> Union[list[list], HttpError]:
        """

        """
        try:
            if not spreadsheet_id:
                spreadsheet_id = GoogleSheets.SAMPLE_SPREADSHEET_ID

            range_names = [
                # Range names ...
            ]
            result = self.service.spreadsheets().values().batchGet(
                spreadsheetId=spreadsheet_id, ranges=_range_names).execute()
            ranges = result.get('valueRanges', [])
            print(f"{len(ranges)} ranges retrieved")
            result = [val['values'] for val in result['valueRanges']]
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def batch_update_values(self, spreadsheet_id: str = None, range_name: str = 'A1',
                            value_input_option: str = "USER_ENTERED",
                            _values: list[list[str]] = [['1']]) -> Union[dict, HttpError]:
        """

        """
        try:
            if not spreadsheet_id:
                spreadsheet_id = GoogleSheets.SAMPLE_SPREADSHEET_ID

            data = [
                {
                    'range': range_name,
                    'values': _values
                },
                # Additional ranges to update ...
            ]
            body = {
                'valueInputOption': value_input_option,
                'data': data
            }
            result = self.service.spreadsheets().values().batchUpdate(
                spreadsheetId=spreadsheet_id, body=body).execute()
            print(f"{(result.get('totalUpdatedCells'))} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def get_tasks(self, spreadsheet_id: str = None, range_name: str = 'A2:A100'):
        """
        """
        try:
            if not spreadsheet_id:
                spreadsheet_id = GoogleSheets.SAMPLE_SPREADSHEET_ID

            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            rows = [i for line in result.get('values', []) for i in line]
            print(f"{len(rows)} rows retrieved")

            return rows
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def get_ready_tasks(self, spreadsheet_id: str = None, range_name: str = 'B2:B100'):
        """
        """
        try:
            if not spreadsheet_id:
                spreadsheet_id = GoogleSheets.SAMPLE_SPREADSHEET_ID

            result = self.service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id, range=range_name).execute()
            rows = [i for line in result.get('values', []) for i in line]
            print(f"{len(rows)} rows retrieved")

            return rows
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error

    def add_task(self, spreadsheet_id: str = None, range_name: str = "A2", value_input_option: str = "USER_ENTERED",
                 _values: list[list[str]] = "Новая хадача"):
        """
        """
        try:
            if not spreadsheet_id:
                spreadsheet_id = GoogleSheets.SAMPLE_SPREADSHEET_ID

            values = [
                [
                    # Cell values ...
                ],
                # Additional rows ...
            ]
            body = {
                'values': _values
            }
            result = self.service.spreadsheets().values().update(
                spreadsheetId=spreadsheet_id, range=range_name,
                valueInputOption=value_input_option, body=body).execute()
            print(f"{result.get('updatedCells')} cells updated.")
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return error


if __name__ == '__main__':
    gs = GoogleSheets()
    print(gs.batch_get_values(_range_names="A1:B2"))
    gs.batch_update_values()
