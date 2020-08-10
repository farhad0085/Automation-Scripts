from google_play_scraper import Sort, reviews, app, reviews_all
import csv
import datetime
import pandas as pd

def get_details(app_id):
    output = []

    app_details = app(app_id)

    results, _ = reviews(
        app_id,
        sort=Sort.NEWEST,
        count=3500
    )

    today = datetime.date.today()

    yesterday = today - datetime.timedelta(days=1)
    furtherday = yesterday - datetime.timedelta(days=1)

    for result in results:
        if yesterday.strftime("%Y-%m-%d")==result['at'].strftime("%Y-%m-%d"):
            rows = []
            rows.append(app_details['appId'])
            rows.append(app_details['installs'])
            rows.append(result['content'])
            rows.append(result['score'])
            rows.append(result['at'].strftime("%Y-%m-%d %I:%H %p"))
            output.append(rows)
        
        if furtherday.strftime("%Y-%m-%d")==result['at'].strftime("%Y-%m-%d"):
            break

    return output

def save_all_historical_data(app_id):
    output = []

    app_details = app(app_id)

    results = reviews_all(app_id)

    for result in results:
            rows = []
            rows.append(app_details['appId'])
            rows.append(app_details['installs'])
            rows.append(result['content'])
            rows.append(result['score'])
            rows.append(result['at'].strftime("%Y-%m-%d %I:%H %p"))
            output.append(rows)

    with open(r'output_play_store.csv', 'a', encoding="utf-8") as f:
        writer = csv.writer(f)
        for detail in output:
            writer.writerow(detail)

    return True

if __name__ == '__main__':
    app_id = 'com.fantome.penguinisle'

    details = get_details(app_id)

    df = pd.DataFrame(details)