import GetOldTweets3 as got
from datetime import datetime
from requests_html import HTMLSession
import sys
import os
import json
import urllib
from snscrape.modules.twitter import TwitterUserScraper


def save_json(idd, title, description, time, duration, link, channel):
    obj = {'data': []}
    obj['data'].append({'id': idd})
    obj['data'].append({'description': description})
    obj['data'].append({'title': title})
    obj['data'].append({'channel': channel})
    obj['data'].append({'time': time.strftime("%Y-%m-%d %H:%M:%S")})
    obj['data'].append({'duration': duration})
    obj['data'].append({'url': link})
    # print(obj)
    with open(str(idd) + '.json', 'w') as outfile:
        json.dump(obj, outfile)
    os.rename(str(idd) + '.json', paths + "/" + str(idd) + '.json')
    print("{} Saved".format(idd))


def save_thumbnail(idd, screenshot):
    if not os.path.exists(paths + "/" + str(idd) + '.jpg'):
        urllib.request.urlretrieve(screenshot, str(idd) + ".jpg")
        os.rename(str(idd) + ".jpg", paths + "/" + str(idd) + ".jpg")


def get_token():
    with open('tok.txt', 'r') as f:
        token = f.read()
    return token


def get_headers(token):
    headers = {
        'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
        'Accept': '*/*; q=0.01', 'Referer': 'https://twitter.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'X-Twitter-Active-User': 'yes', 'x-guest-token': token
    }

    return headers


def get_duration(id):
    url = f"https://api.twitter.com/1.1/videos/tweet/config/{id}.json"
    try:
        token = get_token()

        session = HTMLSession()
        response = session.get(url, headers=get_headers(token))

        html = response.json()

        if 'errors' in html:
            print("Changing Token")
            try:
                # print("trying")
                # os.system('python ' + os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[0].replace('videos.py', 'tokenId.py')))
                os.system('python ' + "tokenId.py")
                # print("hello")
            except:
                # os.system('py ' + os.path.join(os.path.dirname(os.path.realpath(__file__)), sys.argv[0].replace('videos.py', 'tokenId.py')))
                os.system('python3.6 ' + "tokenId.py")
            token = get_token()

            response = session.get(url, headers=get_headers(token))
            html = response.json()

        try:
            duration = html['track']['durationMs'] / 1000
        except:
            duration = ""
        try:
            poster = html['posterImage']
        except:
            poster = ""
        return duration, poster

    except Exception as e:
        return False, ''


def get_latest_videos(channel_username):
    # tweetCriteria = got.manager.TweetCriteria().setUsername(channel_username).setMaxTweets(30)
    # tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    tweet_user = TwitterUserScraper(username=channel_username)
    tweets = tweet_user.get_items()

    i = 0
    for tweet in tweets:
        if i < 30:
            tweet_id = tweet.id
            i += 1
        else:
            break
        '''Check if video id already exists'''
        if os.path.exists(paths + "/" + str(tweet_id) + ".no"):
            print("Skipping (novideo) -> " + str(tweet_id))
            continue

        if os.path.exists(paths + "/" + str(tweet_id) + ".json"):
            print("Skipping (already there) -> " + str(tweet_id))
            continue

        duration, thumb = get_duration(tweet_id)

        if duration == False or duration == '' or duration is None:
            print("Not A Video (skipping)")
            '''Creating Temp File So Ignore This Next Time'''
            fh = open(str(tweet_id) + ".no", "w")
            fh.close()
            os.rename(str(tweet_id) + ".no", paths +
                      "/" + str(tweet_id) + ".no")
            continue

        duration = duration
        title = tweet.username
        description = tweet.content
        time = tweet.date
        link = tweet.url
        channel = tweet.username

        save_json(tweet_id, title, description, time, duration, link, channel)
        if '' != thumb:
            save_thumbnail(tweet_id, thumb)
        else:
            print("No Image:" + title)


if __name__ == "__main__":
    channel = sys.argv[1]

    paths = "./Twitter"
    if not os.path.exists(paths):
        os.makedirs(paths)

    get_latest_videos(channel)
    # print(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tokenId.py'))
