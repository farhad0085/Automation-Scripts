import requests
import time
import datetime
import pandas as pd
# import dateparser

subreddit = "Bitcoin"

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"
}


def timestamp_to_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))
    return dt_object


def timestamp_to_datetime(timestamp):
    dt_object = datetime.datetime.fromtimestamp(int(timestamp))
    return dt_object


def get_posts(subreddit, days_ago=120):

    current_date = datetime.datetime.utcnow()
    days_before = current_date - datetime.timedelta(days=days_ago)
    # print(days_before)
    
    posts = []

    main_url = f"https://www.reddit.com/r/{subreddit}/.json"
    next_url = main_url

    loop = 1
    while True:
        print(next_url)
        response = requests.get(next_url, headers=headers).json()
        # print(response)
        childrens = response['data']['children']

        for children in childrens:
            children_data = children['data']

            data = {}

            post_id = children_data['id']
            body = children_data['selftext']
            title = children_data['title']
            author = children_data['author']
            up_votes = children_data['ups']
            down_votes = children_data['downs']
            created_utc = children_data['created_utc']
            url = children_data['url']
            comments = children_data['num_comments']

            data['post_id'] = post_id
            data['body'] = body
            data['title'] = title
            data['author'] = author
            data['up_votes'] = up_votes
            data['down_votes'] = down_votes
            data['created_utc'] = timestamp_to_datetime(created_utc)
            data['url'] = url
            data['comments'] = comments
            # print(data['created_utc'])

            posts.append(data)

            if data['created_utc'] < days_before and loop > 3:
                return posts

        loop += 1

        init_count = 25
        after = response['data']['after']
        next_url = main_url + f"?count={init_count}&after={after}"
        init_count += 25

        print(len(posts), "posts grabbed")

        if len(posts) > 200000:
            break

        time.sleep(0.3)
    return posts


def get_comment_json(subreddit, post_id):
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}/.json"

    response = requests.get(url, headers=headers).json()
    comments_data = response[1]
    return comments_data



def recurr(replies, post_id):

    comments = []

    if replies:
        replies = replies['data']['children']

        for reply in replies:
            comment_data = {}
            replies_data = reply['data']
            try:
                comment_data['body'] = replies_data['body']
                comment_data['created_utc'] = timestamp_to_datetime(replies_data['created_utc'])
                comment_data['subreddit'] = replies_data['subreddit']
                comment_data['post_id'] = post_id
                comment_data['author'] = replies_data['author']
                comments.append(comment_data)
                new_replies_data = replies_data['replies']
            except:
                continue
            
            comments =  comments + recurr(new_replies_data, post_id)
        
        return comments
        

    else:
        return []

def get_comments_data(subreddit, post_id):

    json_data = get_comment_json(subreddit, post_id)

    comments_old = []
    replies = json_data['data']['children']

    for reply in replies:
        
        comment_data = {}
        replies_data = reply['data']
        try:
            comment_data['body'] = replies_data['body']
            comment_data['created_utc'] = timestamp_to_datetime(replies_data['created_utc'])
            comment_data['subreddit'] = replies_data['subreddit']
            comment_data['post_id'] = post_id
            comment_data['author'] = replies_data['author']
            
            new_replies_data = replies_data['replies']
        except:
            continue
        comments = recurr(new_replies_data, post_id)
        comments_old.append(comment_data)

        for item in comments:
            comments_old.append(item)
    print(len(comments_old), "comments grabbed")
    return comments_old



if __name__ == "__main__":
    posts = get_posts(subreddit, days_ago=1)
    df_posts = pd.DataFrame(posts)
    df_posts.to_csv("posts.csv")

    comments = []

    for post in posts:
        comment_data = get_comments_data(subreddit, post['post_id'])

        for c in comment_data:
            comments.append(c)
    print("Total", len(comments), "comments grabbed")
    df_comments = pd.DataFrame(comments)
    df_comments.to_csv("comments.csv")
    # t = timestamp_to_datetime(1596281159.0)
    # print(t)
    