import pandas as pd
import os
import urllib.request

def download_dataset():
    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
    
    os.makedirs('data/raw', exist_ok=True)
    file_path = 'data/raw/default_credit_card_clients.xls'
    
    print(f"Downloading dataset from {url}...")
    urllib.request.urlretrieve(url, file_path)
    print(f"Dataset downloaded to {file_path}")
    
    print("Reading dataset...")
    df = pd.read_excel(file_path, header=1)
    
    csv_path = 'data/raw/default_credit_card_clients.csv'
    df.to_csv(csv_path, index=False)
    print(f"Dataset saved as CSV: {csv_path}")
    
    print(f"Dataset shape: {df.shape}")
    print(f"First 5 rows:")
    print(df.head())
    
    return df

if __name__ == '__main__':
    download_dataset()