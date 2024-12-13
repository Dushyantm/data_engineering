import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import argparse
from time import time
import wget
import gzip
import getpass

def download_csv(url, output_path):
    """Downloads a CSV file, optionally handles gzip compression."""
    try:
        if url.endswith('.gz'):
            downloaded_file = wget.download(url)
            with gzip.open(downloaded_file, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    f_out.write(f_in.read())
            os.remove(downloaded_file)
        else:
            wget.download(url, out=output_path)
        print(f"Downloaded file to {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None


def main(params):
    user = params.user
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    # Use getpass to prompt for the password
    password = getpass.getpass("Enter PostgreSQL Password: ")


    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    try:
        engine.connect()  # Test the connection
        print("Connection to PostgreSQL successful!")
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return  # Exit if connection fails

    # Download the CSV (checking for errors)
    downloaded_file_path = 'yellow_tripdata_2021-01.csv'  # Local file name
    downloaded_file_path = download_csv(url, downloaded_file_path)
    if downloaded_file_path is None:
        return  # Exit if download failed

    df_iter = pd.read_csv(downloaded_file_path, iterator=True, chunksize=100000)

    # Get the first chunk and create the table
    df_chunked = next(df_iter)
    df_chunked.tpep_pickup_datetime = pd.to_datetime(df_chunked.tpep_pickup_datetime)
    df_chunked.tpep_dropoff_datetime = pd.to_datetime(df_chunked.tpep_dropoff_datetime)

    try:  # Handle potential errors during table creation
        df_chunked.head(0).to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error creating table: {e}")
        return

    # Insert data in chunks
    df_chunked.to_sql(name=table_name, con=engine, if_exists='append', index=False)  # First chunk
    while True:
        t_start = time()
        try:
            df_chunk = next(df_iter)
            df_chunk.tpep_pickup_datetime = pd.to_datetime(df_chunk.tpep_pickup_datetime)
            df_chunk.tpep_dropoff_datetime = pd.to_datetime(df_chunk.tpep_dropoff_datetime)
            df_chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            t_end = time()
            print(f"Inserted another chunk, took {t_end - t_start:.3f} seconds")

        except StopIteration:
            print("Finished ingesting data into PostgreSQL.")
            break
        except Exception as e: # Catch other potential errors during insertion
            print(f"Error inserting chunk: {e}")
            break  # Or choose to handle the error differently



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data into PostgreSQL.')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres', type=int)
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table')
    parser.add_argument('--url', required=True, help='url of the csv file')

    args = parser.parse_args()

    main(args)