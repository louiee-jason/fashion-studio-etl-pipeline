import pytest
from unittest.mock import patch, MagicMock
from utils.load import load_to_csv, load_to_postgres, load_to_google_sheets, load_data
import pandas as pd
import os

@patch('utils.load.pd.DataFrame.to_csv')
def test_load_to_csv(mock_to_csv):
    df = pd.DataFrame({'col': [1, 2]})
    load_to_csv(df, 'test.csv')
    mock_to_csv.assert_called_once_with('test.csv', index=False)

@patch('utils.load.create_engine')
@patch('utils.load.pd.DataFrame.to_sql')
def test_load_to_postgres(mock_to_sql, mock_create_engine):
    df = pd.DataFrame({'col': [1, 2]})
    load_to_postgres(df, 'sqlite:///:memory:')
    mock_create_engine.assert_called_once()
    mock_to_sql.assert_called_once()

@patch('os.path.exists')
@patch('utils.load.service_account.Credentials.from_service_account_file')
@patch('utils.load.build')
def test_load_to_google_sheets(mock_build, mock_creds, mock_exists):
    mock_exists.return_value = True
    
    mock_service = MagicMock()
    mock_build.return_value = mock_service
    
    mock_spreadsheets = MagicMock()
    mock_service.spreadsheets.return_value = mock_spreadsheets
    
    mock_values = MagicMock()
    mock_spreadsheets.values.return_value = mock_values
    
    mock_update = MagicMock()
    mock_values.update.return_value = mock_update
    
    mock_execute = MagicMock()
    mock_execute.get.return_value = 2
    mock_update.execute.return_value = mock_execute
    
    df = pd.DataFrame({'col': [1, 2]})
    load_to_google_sheets(df, 'dummy_id', 'dummy_file.json')
    
    mock_build.assert_called_once()
    mock_values.update.assert_called_once()

@patch('utils.load.load_to_csv')
@patch('utils.load.load_to_postgres')
@patch('utils.load.load_to_google_sheets')
def test_load_data(mock_sheets, mock_pg, mock_csv):
    df = pd.DataFrame({'col': [1, 2]})
    load_data(df)
    mock_csv.assert_called_once_with(df)
    mock_pg.assert_called_once_with(df)
    mock_sheets.assert_called_once_with(df)
