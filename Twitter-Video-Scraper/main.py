import json
import os
import re
import sys
import time
import urllib
from datetime import datetime

from requests_html import HTMLSession, HTML


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


def get_duration(id):
    url1 = "https://api.twitter.com/1.1/videos/tweet/config/{}.json".format(id)
    try:
        f = open('tok.txt', 'r')
        token = f.read()
        f.close()
        header1 = {
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'Accept': '*/*; q=0.01', 'Referer': 'https://twitter.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'X-Twitter-Active-User': 'yes', 'x-guest-token': token
        }
        r1 = session.get(url1, headers=header1)
        print(r1.text)
        html1 = r1.json()
        # print(html1)
        if 'errors' in html1:
            print("Change Token")
            try:
                os.system('python ' + os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                        sys.argv[0].replace('main.py', 'tokenId.py')))
            except:
                os.system('py ' + os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                sys.argv[0].replace('main.py', 'tokenId.py')))
            f = open('tok.txt', 'r')
            token = f.read()
            f.close()
            header1 = {
                'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
                'Accept': '*/*; q=0.01', 'Referer': 'https://twitter.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                'X-Twitter-Active-User': 'yes', 'x-guest-token': token
            }
            r1 = session.get(url1, headers=header1)
            html1 = r1.json()
        print(html1)
        try:
            duration = html1['track']['durationMs'] / 1000
        except:
            duration = ""
        try:
            poster = html1['posterImage']
        except:
            poster = ""
        return duration, poster

    except Exception as e:
        print(e)
        return False, ''


session = HTMLSession()
f = open('tok.txt', 'r')
token = f.read()
f.close()
print(token)
channel = sys.argv[1]
# token="1048158871490052097"
paths = "./Twitter"

if not os.path.exists(paths):
    os.makedirs(paths)

# url = 'https://twitter.com/i/profiles/show/{}/timeline/tweets?include_available_features=1&include_entities=1&include_new_items_bar=true'.format(
#     channel)

url = 'https://twitter.com/{}?include_available_features=1&include_entities=1&include_new_items_bar=true'.format(
    channel)

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Referer': 'https://twitter.com/twittervideo',
           'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8',
           'X-Twitter-Active-User': 'yes',
           'X-Requested-With': 'XMLHttpRequest'}

header1 = {
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAPYXBAAAAAAACLXUNDekMxqa8h%2F40K4moUkGsoc%3DTYfbDKbT3jJPCEVnMYqilB28NHfOPqkca3qaAxGfsyKCs0wRbw',
    'Accept': '*/*; q=0.01', 'Referer': 'https://twitter.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'X-Twitter-Active-User': 'yes', 'x-guest-token': token
}

# r = session.get(url, headers=header1)
# print(r)
# print(r.text)
# sys.exit(1)
ids = ["1296469574796431360",
"1296466170078466052",
"1296465897163546630",
"1296465621979475968",
"1296465558314143744",
"1296465513393119232",
"1296465494397071361",
"1296465441876070400",
"1296465342328446977",
"1296454174767558657",
"1296448916569890818",
"1296445151435522049",
"1296444488550952961",
"1296444332959059972",
"1296441638240301056",
"1296440630562955265",
"1296440599818772480",
"1296440229121921025",
"1296440183181791235",
"1296440111123619844",
"1296439870357987329",
"1296439195448291328"]

# for id in ids:https://twitter.com/i/status/1290269710185947137
get_duration("1290269710185947137")

# print(dir(session))
# print(session.cookies)
# print(html)
# sys.exit()


# try:
#     suspended = r.json()['message'] == "Sorry, that user is suspended."
# except:
#     suspended = ""
# try:
#     testhtml = r.json()['items_html']
# except:
#     testhtml = ''

# # try:
# if 'media may contain sensitive material' in testhtml:
#     suspended = "1"

# if (suspended):
#     sys.exit(1)
# else:
#     html = HTML(html=r.json()['items_html'], url='bunk', default_encoding='utf-8')
#     for tweet in html.find('.stream-item'):
#         try:
#             name = tweet.find('.FullNameGroup')[0].full_text
#             if 'Verified' in name:
#                 name = name[:-17]
#         except:
#             name = ""
#         try:
#             text = tweet.find('.tweet-text')[0].full_text
#             loc1 = text.find('pic.')
#             text = text[:loc1]
#         except:
#             text = ""
#         description = name + ' - ' + text
#         try:
#             title = tweet.xpath('//div[@class="PlayableMedia-title"]/text()')[0]

#         except:
#             title = ""
#         print("TITLE:[" + title + "]")
#         try:
#             tweetId = tweet.find('.js-permalink')[0].attrs['data-conversation-id']
#         except:
#             tweetId = ""
#         # print(tweetId)
#         try:
#             time = datetime.fromtimestamp(int(tweet.find('._timestamp')[0].attrs['data-time-ms']) / 1000.0)
#         except:
#             time = ""
#         try:
#             link = "https://twitter.com" + tweet.find('.tweet-timestamp')[0].attrs['href']
#         except:
#             link = ""
#         '''
#         try:
#             thumb = tweet.find('.PlayableMedia-player')[0].attrs['style']
#             t1 = thumb.find("('")
#             t2 = thumb.find("')")
#             thumb = thumb[t1 + 2:t2]
#         except:
#             thumb =""
#         '''
#         '''Check if video id already exists'''
#         if os.path.exists(paths + "/" + str(tweetId) + ".no"):
#             print("Skipping (novideo) -> " + tweetId)
#         else:
#             if os.path.exists(paths + "/" + str(tweetId) + ".json"):
#                 print("Skipping (already there) -> " + tweetId)
#             else:
#                 duration, thumb = get_duration(tweetId)
#                 if duration == False or duration == '' or duration is None:
#                     print("Not A Video (skipping)")
#                     '''Creating Temp File So Ignore This Next Time'''
#                     fh = open(str(tweetId) + ".no", "w")
#                     fh.close()
#                     os.rename(str(tweetId) + ".no", paths + "/" + str(tweetId) + ".no")
#                 else:
                    # save_json(tweetId, title, description, time, duration, link, channel)
#                     if '' != thumb:
#                         save_thumbnail(tweetId, thumb)
#                     else:
#                         print("No Image:" + title)
# # except:
# #     pass
# #     pass
