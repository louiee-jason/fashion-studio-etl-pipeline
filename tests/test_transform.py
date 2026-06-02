import pytest
import pandas as pd
from utils.transform import transform_data, clean_price, clean_rating, clean_colors, clean_size, clean_gender

def test_clean_price():
    assert clean_price("$15.50") == 248000.0
    assert clean_price("Price Unavailable") is None
    assert clean_price(None) is None
    assert clean_price("invalid") is None

def test_clean_rating():
    assert clean_rating("4.8 / 5") == 4.8
    assert clean_rating("Invalid Rating") is None
    assert clean_rating(None) is None

def test_clean_colors():
    assert clean_colors("3 Colors") == 3
    assert clean_colors(None) is None

def test_clean_size():
    assert clean_size("Size: M") == "M"
    assert clean_size("M") == "M"

def test_clean_gender():
    assert clean_gender("Gender: Men") == "Men"
    assert clean_gender("Men") == "Men"

def test_transform_data():
    raw_data = {
        'Title': ['T-Shirt A', 'T-Shirt B', 'T-Shirt C', 'Unknown Product', 'T-Shirt A'],
        'Price': ['$10.00', 'Price Unavailable', '$20.00', '$10.00', '$10.00'],
        'Rating': ['4.0 / 5', '4.5 / 5', 'Invalid Rating', '4.0 / 5', '4.0 / 5'],
        'Colors': ['3 Colors', '2 Colors', '1 Colors', '3 Colors', '3 Colors'],
        'Size': ['Size: S', 'Size: M', 'Size: L', 'Size: S', 'Size: S'],
        'Gender': ['Gender: Men', 'Gender: Women', 'Gender: Men', 'Gender: Men', 'Gender: Men'],
        'timestamp': ['2023-01-01T12:00:00', '2023-01-01T12:00:00', '2023-01-01T12:00:00', '2023-01-01T12:00:00', '2023-01-01T12:00:00']
    }
    df = pd.DataFrame(raw_data)
    
    cleaned_df = transform_data(df)
    
    # Check that duplicates, invalid titles, and None values were dropped
    # Row 0: valid -> kept
    # Row 1: invalid price ("Price Unavailable" -> None) -> dropped
    # Row 2: invalid rating ("Invalid Rating" -> None) -> dropped
    # Row 3: "Unknown Product" title -> dropped
    # Row 4: duplicate of row 0 -> dropped
    assert len(cleaned_df) == 1
    
    # Check that transformations are applied
    row = cleaned_df.iloc[0]
    assert row['Price'] == 160000.0  # 10 * 16000
    assert row['Rating'] == 4.0
    assert row['Colors'] == 3
    assert row['Size'] == 'S'
    assert row['Gender'] == 'Men'
