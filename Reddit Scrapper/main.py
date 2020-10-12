import datetime
import requests
import time
import pandas as pd



def timestamp_to_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    return dt_object

def datetime_to_timestamp(dt):
    timestamp = datetime.datetime.timestamp(dt)
    return timestamp




def get_all_posts(subreddit):

    current_date = datetime.datetime.utcnow()
    before_15_hours = current_date - datetime.timedelta(hours=15)

    posts = []

    while True:

        current_date_timestamp = int(datetime_to_timestamp(current_date))
        before_15_hours_timestamp = int(datetime_to_timestamp(before_15_hours))

        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&sort=desc&sort_type=created_utc&after={before_15_hours_timestamp}&before={current_date_timestamp}&size=100"

        response = requests.get(url).json()
        if len(response['data']) == 0:
            break

        for datum in response['data']:
            new_data = {}
            new_data['created_utc'] = datum['created_utc']
            new_data['post_id'] = datum['id']
            new_data['subreddit'] = datum['subreddit']
            new_data['title'] = datum['title']
            new_data['body'] = datum['selftext']
            posts.append(new_data)

        current_date = before_15_hours
        before_15_hours = before_15_hours - datetime.timedelta(hours=15)

        print(len(posts), "posts grabbed")
        time.sleep(0.1)

    return posts


def get_4months_posts(subreddit):

    current_date = datetime.datetime.utcnow()
    before_15_hours = current_date - datetime.timedelta(hours=15)
    before_4_month = current_date - datetime.timedelta(days=120)

    posts = []

    while current_date > before_4_month:

        current_date_timestamp = int(datetime_to_timestamp(current_date))
        before_15_hours_timestamp = int(datetime_to_timestamp(before_15_hours))

        url = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&sort=desc&sort_type=created_utc&after={before_15_hours_timestamp}&before={current_date_timestamp}&size=100"

        response = requests.get(url).json()
        if len(response['data']) == 0:
            break

        for datum in response['data']:
            new_data = {}
            new_data['created_utc'] = timestamp_to_datetime(datum['created_utc'])
            new_data['post_id'] = datum['id']
            new_data['subreddit'] = datum['subreddit']
            new_data['title'] = datum['title']
            try:
                new_data['body'] = datum['selftext']
            except:
                new_data['body'] = ""
            posts.append(new_data)

        current_date = before_15_hours
        before_15_hours = before_15_hours - datetime.timedelta(hours=15)

        print(len(posts), "posts grabbed")
        time.sleep(0.1)

    return posts


def get_comment_ids(post_id):
    endpoint = f"https://api.pushshift.io/reddit/submission/comment_ids/{post_id}"
    response = requests.get(endpoint).json()
    return response['data']

def get_comments_data(comment_id):
    endpoint = f"https://api.pushshift.io/reddit/comment/search?ids={comment_id}"
    response = requests.get(endpoint).json()['data'][0]
    data = {}
    data['body'] = response['body']
    data['created_utc'] = timestamp_to_datetime(response['created_utc'])
    data['post_id'] = response['link_id']
    data['subreddit'] = response['subreddit']
    return data

def get_all_comments(posts):
    comment = []
    for post in posts:
        comment_ids = get_comment_ids(post['post_id'])

        for comment_id in comment_ids:
            try:
                comment_data = get_comments_data(comment_id)
                comment.append(comment_data)
                print(len(comment), "Comments grabbed")
            except:
                continue

if __name__ == "__main__":
    posts = get_4months_posts("bitcoin")
    comments = get_all_comments(posts)

    df_posts = pd.DataFrame(posts)
    df_comments = pd.DataFrame(comments)