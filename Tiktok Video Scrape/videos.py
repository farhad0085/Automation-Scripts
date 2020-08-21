from TikTokApi import TikTokApi
import datetime
import io
import json
import logging
import os
import re
import shutil
import socket
import sys
import datetime
from urllib import request, parse, error

import bs4
import requests




def get_video_infos(id):

    try:
        tiktok = api.getTikTokById(id=id)
        # print(tiktok)
        http_proxy = "5.79.73.131:13080"

        proxyDict = {
            "https": http_proxy,
        }

        video_data = tiktok['itemInfo']['itemStruct']['video']
        share_meta = tiktok['itemInfo']['shareMeta']
        print(share_meta['title'])
        url = "https://www.tiktok.com/share/video/" + str(id)
        timestamp = datetime.datetime.fromtimestamp(tiktok['itemInfo']['itemStruct']['createTime']).strftime("%Y-%m-%d %H:%M:%S")

        my_json = {"duration": video_data['duration'],
                    "description": share_meta['title'],
                    "title": share_meta['desc'],
                    "timestamp": timestamp,
                    "url": url,
                    "poster_url": video_data['cover']}

        with open(main_json_dir + '/' + str(url).split('/')[-1] + '.json', 'w', encoding='utf-8') as f:
                json.dump(my_json, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print("This Url didn't work:",
              'https://t.tiktok.com/i18n/share/video/' + id)
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)
        return False


if __name__ == "__main__":
    
    api = TikTokApi()
    main_json_dir = './tiktok-data'

    try:
        file_ = '-' + str(sys.argv[1])
    except:
        file_ = ''
    txt_file = 'IDs' + file_ + '.txt'
    if not os.path.exists(main_json_dir):
        os.mkdir(main_json_dir)

    with open(txt_file, 'r') as f:
        ids = f.read().split('\n')

    for id in ids:
        if id != '' and id != None:
            print('Processing:', id)
            try:
                if not os.path.exists(main_json_dir + '/' + str(id) + '.json'):
                    get_video_infos(id)
                else:
                    print('Already Here:', main_json_dir + '/' + str(id) + '.json')
            except:
                print("This Url didn't work:",
                      'https://www.tiktok.com/share/video/' + id)
                pass

    try:
        dir = 'To Delete'

        if os.path.exists(dir):
            shutil.rmtree(dir)
    except:
        pass