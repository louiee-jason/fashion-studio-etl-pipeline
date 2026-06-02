import pandas as pd
from sqlalchemy import create_engine
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

logging.basicConfig(level=logging.INFO)

def load_to_csv(df, filename='products.csv'):
    try:
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to CSV: {filename}")
    except Exception as e:
        logging.error(f"Error saving to CSV: {e}")
        raise e

def load_to_postgres(df, connection_string='postgresql://postgres:postgres@localhost:5432/fashion_db'):
    try:
        engine = create_engine(connection_string)
        df.to_sql('products', engine, if_exists='replace', index=False)
        logging.info("Data successfully saved to PostgreSQL database")
    except Exception as e:
        logging.error(f"Error saving to PostgreSQL: {e}")
        pass

def load_to_google_sheets(df, spreadsheet_id='1w1IjoBjTYNsMqHeJKKbqo-mb7SyRPK2xXl-xZfKqqeY', credentials_file='google-sheets-api.json'):
    try:
        if not os.path.exists(credentials_file):
            logging.warning(f"File kredensial '{credentials_file}' nggak ketemu. Skip upload ke Google Sheets.")
            return

        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(credentials_file, scopes=scopes)
        service = build('sheets', 'v4', credentials=creds)

        values = [df.columns.tolist()] + df.astype(str).values.tolist()
        
        body = {
            'values': values
        }
        
        range_name = 'Sheet1!A1'
        
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption='USER_ENTERED', body=body).execute()
        
        logging.info(f"{result.get('updatedCells')} cells updated in Google Sheets")
    except Exception as e:
        logging.error(f"Error saving to Google Sheets: {e}")
        pass

def load_data(df):
    load_to_csv(df)
    load_to_postgres(df)
    load_to_google_sheets(df)
