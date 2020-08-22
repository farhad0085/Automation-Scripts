import requests
import pandas as pd
import csv
from datetime import datetime, timedelta

def download_csv(stock_name):
    stocks_path = './Stocks_Data/'
    csv_url = f'https://robintrack.net/api/stocks/{stock_name}/popularity_history_csv'
    response = requests.get(csv_url)
    csv_content = response.text

    filepath = stocks_path+stock_name+'.csv'

    with open(filepath, 'w+', encoding='utf-8') as f:
        f.write(csv_content)

    return filepath


def get_last_hour():
    last_hour_date_time = datetime.utcnow() - timedelta(hours = 1)
    return last_hour_date_time.strftime('%Y-%m-%d %H')


def get_last_hour_data(csv_file):
    last_hour = get_last_hour()
    last_hour_data = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0][:-10] == last_hour:
                last_hour_data.append(row)

    return last_hour_data


if __name__ == "__main__":
    stock = "MSFT"
    filename = download_csv(stock)
    last_hour_data = get_last_hour_data(filename)
    df = pd.DataFrame(last_hour_data)
    print(df)