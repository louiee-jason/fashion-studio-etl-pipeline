import pytest
from unittest.mock import patch, MagicMock
from utils.extract import scrape_main
import pandas as pd

@patch('utils.extract.requests.Session')
def test_scrape_main(mock_session_class):
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    # Simulate HTML response
    mock_response.text = """
    <html><body>
        <div class="product-card">
            <h3 class="title">T-Shirt Men</h3>
            <div class="price">$15.50</div>
            <div class="rating">4.8 / 5</div>
            <div class="color">3 Colors</div>
            <div class="size">Size: M</div>
            <div class="gender">Gender: Men</div>
        </div>
    </body></html>
    """
    mock_session.get.return_value = mock_response
    
    df = scrape_main(total_pages=1)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert df.iloc[0]['Title'] == 'T-Shirt Men'
    assert df.iloc[0]['Price'] == '$15.50'
    assert df.iloc[0]['Rating'] == '4.8 / 5'
    assert df.iloc[0]['Colors'] == '3 Colors'
    assert df.iloc[0]['Size'] == 'Size: M'
    assert df.iloc[0]['Gender'] == 'Gender: Men'
    assert 'timestamp' in df.columns

@patch('utils.extract.requests.Session')
def test_scrape_main_error_handling(mock_session_class):
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    
    import requests
    # Simulate a request exception
    mock_session.get.side_effect = requests.exceptions.RequestException("Mocked Error")
    
    df = scrape_main(total_pages=1)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
