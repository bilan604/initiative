import numpy as np
import pandas as pd

import gspread
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials


def get_authorized_client(scope=[], path='credentials.json'):
    if not scope:
        scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    filename = path
    creds = ServiceAccountCredentials.from_json_keyfile_name(filename, scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    return client

def get_sheet_instance(sheet, sheet_index=0):
    return sheet.get_worksheet(sheet_index)

def get_df(sheet_instance):
    return pd.DataFrame.from_dict(sheet_instance.get_all_records())

def convert_df_to_mtx(df):
    columns = list(df.columns)
    mtx = [columns]
    for i in range(len(df)):
        row = []
        for j in range(len(columns)):
            row.append(df.iloc[i][j])
        mtx.append(row)
    return mtx

def get_mtx_from_sheet_instance(sheet_instance):
    df = get_df(sheet_instance)
    mtx = convert_df_to_mtx(df)
    return mtx

def add_row_to_sheet(row, mtx, sheet_instance):
    m = len(mtx)
    n = len(mtx[0])
    for j in range(n):
        value = str(row[j])
        print(value)
        sheet_instance.update_cell(m+1, j+1, value)

def update_sheet_instance_with_mtx(sheet_instance, mtx):
    # !!! broken, doesn't update all the values
    for i in range(len(mtx)):
        for j in range(len(mtx)):
            value = mtx[i][j]
            if type(mtx[i][j]) == np.int64:
                value = str(value)
            sheet_instance.update_cell(i+1, j+1, value)
    return sheet_instance

def update_sheet_with_data(sheet_name: str, data: dict):
    # data should have keys that are the column names of the sheet
    client = get_authorized_client()

    # get the instance of the Spreadsheet
    sheet = client.open(sheet_name)

    sheet_instance = get_sheet_instance(sheet, 0)

    mtx = get_mtx_from_sheet_instance(sheet_instance)

    row = []
    for col_name in mtx[0]:
        if col_name not in data:
            row.append("")
        else:
            row.append(data[col_name])
    sheet_instance = add_row_to_sheet(row, mtx, sheet_instance)  # mtx's first row is the column names

    return None


