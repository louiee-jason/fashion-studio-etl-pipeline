import logging
from utils.extract import scrape_main
from utils.transform import transform_data
from utils.load import load_data

logging.basicConfig(level=logging.INFO)

def main():
    try:
        logging.info("Starting ETL Pipeline")
        
        logging.info("Extracting data from website")
        df_raw = scrape_main(total_pages=50)
        
        if df_raw.empty:
            logging.error("No data extracted")
            return

        logging.info("Transforming data")
        df_clean = transform_data(df_raw)
        
        if df_clean.empty:
            logging.error("No data left after transformation")
            return
            
        logging.info("Loading data to repositories")
        load_data(df_clean)
        
        logging.info("ETL Pipeline finished successfully")
        
    except Exception as e:
        logging.error(f"ETL Pipeline failed: {e}")

if __name__ == "__main__":
    main()
