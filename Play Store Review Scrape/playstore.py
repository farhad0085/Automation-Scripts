import csv
from google_play_scraper import app, reviews


app_id = input('Enter app ip: (example: com.facebook.katana) ')

reviews_obj = app(app_id)

print(f"Total comments : {reviews_obj['reviews']}")

comment_limit = input("How much comments you want to scrape (Enter ALL to scrape all comments. Highest is 12210): ")

if comment_limit == 'ALL':
    comment_limit = int(reviews_obj['reviews'])
else:
    comment_limit = int(comment_limit)

results, _ = reviews(app_id, count=comment_limit)


for result in results:
    data = []

    comment = result['content']
    rating = result['score']
    comment_date = result['at']

    data.append(comment)
    data.append(rating)
    data.append(comment_date)

    # save the data to csv file
    with open('comments.csv', 'a+') as f:
        writer = csv.writer(f)
        writer.writerow(data)

print(f"{len(results)} data appended to csv")
