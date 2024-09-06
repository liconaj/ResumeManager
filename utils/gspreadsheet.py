from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from typing import Any

class GSpreadSheet:
    def __init__(self, sheet_id: str, range_name: str, readonly: bool = True):
        self.sheet_id = sheet_id
        self.range_name = range_name
        self.readonly = readonly
        self.creds = self._get_credentials()
        self.service = build('sheets', 'v4', credentials=self.creds)

    def _get_credentials(self) -> Credentials:
        readonly_text = ".readonly" if self.readonly else ""
        scopes = [f'https://www.googleapis.com/auth/spreadsheets{readonly_text}']
        return Credentials.from_service_account_file('credentials.json', scopes=scopes)

    def get_raw_data(self) -> list[list[Any]]:
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=self.sheet_id, range=self.range_name).execute()
        data = result.get('values', [])
        if not data:
            return []
        max_columns = len(data[0])
        for row in data:
            if len(row) < max_columns:
                row.extend([''] * (max_columns - len(row)))

        return data

    def parse_data(self, data: list[list[str]]) -> list[dict[str, Any]]:
        if not data or len(data) < 2:
            return []

        headers = data[0]
        profiles = []
        for row in data[1:]:
            if len(row) == len(headers):
                profile = dict(zip(headers, row))
                profiles.append(profile)
            else:
                print(row[0], len(row))
        return profiles

    def fetch_data(self) -> list[dict[str, Any]]:
        raw_data = self.get_raw_data()
        return self.parse_data(raw_data)

    def update_sheet(self, values: list[list[Any]]) -> None:
        if self.readonly:
            raise PermissionError("La hoja de cálculo está en modo solo lectura.")

        body = {'values': values}
        sheet = self.service.spreadsheets()
        sheet.values().update(spreadsheetId=self.sheet_id, range=self.range_name, valueInputOption='RAW', body=body).execute()
