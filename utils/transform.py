import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def clean_price(price_str):
    if pd.isna(price_str):
        return None
    price_str = str(price_str).strip()
    if price_str == "Price Unavailable":
        return None
    try:
        if price_str.startswith('$'):
            val = float(price_str.replace('$', '').replace(',', ''))
            return val * 16000
    except ValueError:
        pass
    return None

def clean_rating(rating_str):
    if pd.isna(rating_str):
        return None
    rating_str = str(rating_str).strip()
    if rating_str == "Invalid Rating":
        return None
    try:
        val = rating_str.split('/')[0].strip()
        return float(val)
    except Exception:
        return None

def clean_colors(color_str):
    if pd.isna(color_str):
        return None
    color_str = str(color_str).strip()
    try:
        val = color_str.split(' ')[0].strip()
        return int(val)
    except Exception:
        return None

def clean_size(size_str):
    if pd.isna(size_str):
        return None
    size_str = str(size_str).strip()
    if size_str.startswith("Size:"):
        return size_str.replace("Size:", "").strip()
    return size_str

def clean_gender(gender_str):
    if pd.isna(gender_str):
        return None
    gender_str = str(gender_str).strip()
    if gender_str.startswith("Gender:"):
        return gender_str.replace("Gender:", "").strip()
    return gender_str

def transform_data(df):
    try:
        df = df.drop_duplicates()
        
        df = df[df['Title'].notna()]
        df = df[df['Title'] != 'Unknown Product']
        
        df['Price'] = df['Price'].apply(clean_price)
        df['Rating'] = df['Rating'].apply(clean_rating)
        df['Colors'] = df['Colors'].apply(clean_colors)
        df['Size'] = df['Size'].apply(clean_size)
        df['Gender'] = df['Gender'].apply(clean_gender)
        
        df = df.dropna()
        
        df['Price'] = df['Price'].astype(float)
        df['Rating'] = df['Rating'].astype(float)
        df['Colors'] = df['Colors'].astype(int)
        df['Size'] = df['Size'].astype(str)
        df['Gender'] = df['Gender'].astype(str)
        df['Title'] = df['Title'].astype(str)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        logging.info(f"Data transformation successful. Row count: {len(df)}")
        return df
    except Exception as e:
        logging.error(f"Error during data transformation: {e}")
        raise e
