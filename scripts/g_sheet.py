import gspread
import os
from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://www.googleapis.com/auth/drive"]


def fetch_gsheet_data(sheet_name, cred_file_path=os.path.join('scripts', 'creds.json')):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(cred_file_path, scope)
    client = gspread.authorize(credentials)
    sheet = client.open(sheet_name).sheet1
    data = sheet.get_all_records()
    return (sheet, data)

def add_candidate_data(candidate_data):
    applied_candidates_sheet, applied_candidates_data = fetch_gsheet_data(sheet_name='Candidates-List')
    row_data = candidate_data
    if applied_candidates_sheet.insert_row(row_data, len(applied_candidates_data)+2):
        return 1
    return 0



