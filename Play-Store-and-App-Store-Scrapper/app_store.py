from app_store_scraper import AppStore
from pprint import pprint
import requests
import random
import datetime
import pandas as pd

def get_app_details(app_id, country):
    LOOKUP_URL = 'https://itunes.apple.com/lookup'

    url = f"{LOOKUP_URL}?id={app_id}&country={country}&entity=software"

    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
    ]

    user_agent = random.choice(user_agents)

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", 
        "Accept-Encoding": "gzip, deflate", 
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8", 
        "Dnt": "1",
        "Upgrade-Insecure-Requests": "1", 
        "User-Agent": user_agent
    }

    response = requests.get(url, headers=headers).json()

    output = []

    try:
        output_dict = {}
        output_dict['app_id'] = response['results'][0]['bundleId']
        output_dict['app_description'] = response['results'][0]['description']
        output_dict['app_version'] = response['results'][0]['version']
        output_dict['json_response'] = response

        output.append(output_dict)
    except:
        print("Something is wrong")

    return output


def get_app_reviews(app_id, country, bundleId):
    fortnite = AppStore(country=country, app_id=app_id, app_name='')
    fortnite.review(how_many=20)

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    furtherday = yesterday - datetime.timedelta(days=1)

    output = []
    for review in fortnite.reviews:
        if yesterday.strftime("%Y-%m-%d") == review['date'].strftime("%Y-%m-%d"):
            my_dict = {}
            my_dict['app_id'] = bundleId
            my_dict['date'] = review['date'].strftime("%Y-%m-%d %I:%H %p")
            my_dict['rating'] = review['rating']
            my_dict['review'] = review['review']
            output.append(my_dict)

        if furtherday.strftime("%Y-%m-%d") == review['date'].strftime("%Y-%m-%d"):
            break

    return output

if __name__ == "__main__":
    
    app_id = "284882215"
    country = 'us'

    app_details = get_app_details(app_id, country)
    app_reviews = get_app_reviews(app_id, country, app_details[0]['app_id'])

    app_detail_df = pd.DataFrame(app_details)
    app_reviews_df = pd.DataFrame(app_reviews)
    
    app_detail_df.to_html("asdfasdf.html")
    app_reviews_df.to_html("asdfaafdssdf.html")