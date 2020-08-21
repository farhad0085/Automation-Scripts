import io
import json
import logging
import os
import re
import shutil
import socket
import sys
from datetime import datetime
from urllib import request, parse, error

import bs4
import requests

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')
fake_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # noqa
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    # noqa
}


def r1(pattern, text):
    m = re.search(pattern, text)
    # print(m)
    if m:
        return m.group(1)


def tiktok_download(url, output_dir='.', merge=True, info_only=True, **kwargs):
    http_proxy = "5.79.73.131:13080"

    proxyDict = {
        "https": http_proxy,
    }

    response = requests.get(url, headers=fake_headers, proxies=proxyDict)

    html = response.text

    # soup = bs4.BeautifulSoup(html, 'lxml')
    try:
        dataText = '{' + \
                   html[html.find('type="application/ld+json" id="videoObject">'):].split('{', 1)[1].split('</script>')[
                       0]
        data = json.loads(dataText)
        # print(data)
        tings = html.split('<title>')[1].split('</title>')[0].strip()
        title = tings.split('TikTok:')[0].strip() + ' TikTok'
        try:
            desc = tings.split('TikTok:')[1].strip()
        except:
            desc = ''
        # video_id = r1(r'/video/(\d+)', url) or r1(r'musical\?id=(\d+)', html)
        # title = '%s [%s]' % (title, video_id)
        # print(title, desc, video_id)

        # print(data)
        # print(data)
        # print(json.dumps(data))
        # source = 'http:' + data['video']['play_addr']['url_list'][0]
        # poster = 'http:' + data['video']['cover']['url_list'][0]
        # try:
        #     music_name = data['/@:uniqueId/video/:id']['videoData']['musicInfos']['musicName']
        #
        # except:
        #     music_name = ''

        duration = data['duration'].replace('PT', '').replace('S', '')
        poster = data['thumbnailUrl'][0]
        # try:
        #     unique_id = data['/@:uniqueId/video/:id']['videoData']['authorInfos']['unique_id']
        # except:
        #     unique_id = ''

        # title = title + '\n' + unique_id + '\n' + music_name
        # title = title.strip()
        timestamp_ = data['uploadDate']

        # res = requests.head(timestamp_)
        # frmt = "%a, %d %b %Y %H:%M:%S GMT"
        # print(res.headers['Last-Modified'])
        # timestamp_ = datetime.strptime(res.headers['Last-Modified'], frmt)

        # timestamp_ = 1
        # mime, ext, size = url_info(source)data['create_time'] or ''
        # print(poster)

        dir = 'To Delete'

        if os.path.exists(dir):
            shutil.rmtree(dir)

        # try:
        #     os.mkdir(dir)
        # except:
        #     pass

        # urllib.request.urlretrieve(
        # source,
        # dir + '/' + video_id + '.mp4')

        # clip = VideoFileClip(dir + '/' + video_id + '.mp4')
        # clip.close()
        my_json = {"duration": str(duration), "title": title,
                   "description": desc,
                   "timestamp": str(timestamp_),
                   "url": url,
                   "poster_url": poster}

        # print(my_json)

        with open(main_json_dir + '/' + str(url).split('/')[-1] + '.json', 'w', encoding='utf-8') as f:
            json.dump(my_json, f, indent=4)
        # print(url, title, mime, size, source)
        # if not info_only:
        #     download_urls([source], title, ext, size, output_dir, merge=merge)
    except Exception as e:
        print("This Url didn't work:",
              'https://t.tiktok.com/i18n/share/video/' + id)
        print('Error on line {}'.format(
            sys.exc_info()[-1].tb_lineno), type(e).__name__, e)


def get_html(url, encoding=None, faker=False):
    content = get_response(url, faker)
    return str(content, 'utf-8', 'ignore')


def get_response(url, faker=False):
    logging.debug('get_response: %s' % url)

    # install cookies
    cookies = False
    if cookies:
        opener = request.build_opener(request.HTTPCookieProcessor(cookies))
        request.install_opener(opener)

    if faker:
        http_proxy = "http://10.10.1.10:3128"
        https_proxy = "https://10.10.1.11:1080"
        ftp_proxy = "ftp://10.10.1.10:3128"

        proxyDict = {
            "http": http_proxy,
            "https": https_proxy,
            "ftp": ftp_proxy
        }

        response = requests.get(url, headers=fake_headers)
        # requ_ = request.Request(url, headers=fake_headers)
    else:
        response = request.urlopen(url)

    data = response.text
    # if response.info().get('Content-Encoding') == 'gzip':
    #     data = ungzip(data)
    # elif response.info().get('Content-Encoding') == 'deflate':
    #     data = undeflate(data)
    # response.data = data
    return data


def ungzip(data):
    """Decompresses data for Content-Encoding: gzip.
    """
    from io import BytesIO
    import gzip
    buffer = BytesIO(data)
    f = gzip.GzipFile(fileobj=buffer)
    return f.read()


def url_info(url, faker=False, headers={}):
    logging.debug('url_info: %s' % url)

    if faker:
        response = urlopen_with_retry(
            request.Request(url, headers=fake_headers)
        )
    elif headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(request.Request(url))

    headers = response.headers

    type = headers['content-type']
    if type == 'image/jpg; charset=UTF-8' or type == 'image/jpg':
        type = 'audio/mpeg'  # fix for netease
    mapping = {
        'video/3gpp': '3gp',
        'video/f4v': 'flv',
        'video/mp4': 'mp4',
        'video/MP2T': 'ts',
        'video/quicktime': 'mov',
        'video/webm': 'webm',
        'video/x-flv': 'flv',
        'video/x-ms-asf': 'asf',
        'audio/mp4': 'mp4',
        'audio/mpeg': 'mp3',
        'audio/wav': 'wav',
        'audio/x-wav': 'wav',
        'audio/wave': 'wav',
        'image/jpeg': 'jpg',
        'image/png': 'png',
        'image/gif': 'gif',
        'application/pdf': 'pdf',
    }
    if type in mapping:
        ext = mapping[type]
    else:
        type = None
        if headers['content-disposition']:
            try:
                filename = parse.unquote(
                    r1(r'filename="?([^"]+)"?', headers['content-disposition'])
                )
                if len(filename.split('.')) > 1:
                    ext = filename.split('.')[-1]
                else:
                    ext = None
            except:
                ext = None
        else:
            ext = None

    if headers['transfer-encoding'] != 'chunked':
        size = headers['content-length'] and int(headers['content-length'])
    else:
        size = None

    return type, ext, size


def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            return request.urlopen(*args, **kwargs)
        except socket.timeout as e:
            logging.debug('request attempt %s timeout' % str(i + 1))
            if i + 1 == retry_time:
                raise e
        # try to tackle youku CDN fails
        except error.HTTPError as http_error:
            logging.debug('HTTP Error with code{}'.format(http_error.code))
            if i + 1 == retry_time:
                raise http_error


def download_urls(
        urls, title, ext, total_size, output_dir='.', refer=None, merge=True,
        faker=False, headers={}, **kwargs):
    assert urls
    if json_output:
        json_output_.download_urls(
            urls=urls, title=title, ext=ext, total_size=total_size,
            refer=refer
        )
        return
    if dry_run:
        print_user_agent(faker=faker)
        try:
            print('Real URLs:\n%s' % '\n'.join(urls))
        except:
            print('Real URLs:\n%s' % '\n'.join([j for i in urls for j in i]))
        return

    if player:
        launch_player(player, urls)
        return

    if not total_size:
        try:
            total_size = urls_size(urls, faker=faker, headers=headers)
        except:
            import traceback
            traceback.print_exc(file=sys.stdout)
            pass

    title = tr(get_filename(title))
    output_filename = get_output_filename(urls, title, ext, output_dir, merge)
    output_filepath = os.path.join(output_dir, output_filename)

    if total_size:
        if not force and os.path.exists(output_filepath) and not auto_rename \
                and os.path.getsize(output_filepath) >= total_size * 0.9:
            log.w('Skipping %s: file already exists' % output_filepath)
            print()
            return
        bar = SimpleProgressBar(total_size, len(urls))
    else:
        bar = PiecesProgressBar(total_size, len(urls))

    if len(urls) == 1:
        url = urls[0]
        print('Downloading %s ...' % tr(output_filename))
        bar.update()
        url_save(
            url, output_filepath, bar, refer=refer, faker=faker,
            headers=headers, **kwargs
        )
        bar.done()
    else:
        parts = []
        print('Downloading %s.%s ...' % (tr(title), ext))
        bar.update()
        for i, url in enumerate(urls):
            filename = '%s[%02d].%s' % (title, i, ext)
            filepath = os.path.join(output_dir, filename)
            parts.append(filepath)
            bar.update_piece(i + 1)
            url_save(
                url, filepath, bar, refer=refer, is_part=True, faker=faker,
                headers=headers, **kwargs
            )
        bar.done()

        if not merge:
            print()
            return

        if 'av' in kwargs and kwargs['av']:
            from .processor.ffmpeg import has_ffmpeg_installed
            if has_ffmpeg_installed():
                from .processor.ffmpeg import ffmpeg_concat_av
                ret = ffmpeg_concat_av(parts, output_filepath, ext)
                print('Merged into %s' % output_filename)
                if ret == 0:
                    for part in parts:
                        os.remove(part)

        elif ext in ['flv', 'f4v']:
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_flv_to_mp4
                    ffmpeg_concat_flv_to_mp4(parts, output_filepath)
                else:
                    from .processor.join_flv import concat_flv
                    concat_flv(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        elif ext == 'mp4':
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_mp4_to_mp4
                    ffmpeg_concat_mp4_to_mp4(parts, output_filepath)
                else:
                    from .processor.join_mp4 import concat_mp4
                    concat_mp4(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        elif ext == 'ts':
            try:
                from .processor.ffmpeg import has_ffmpeg_installed
                if has_ffmpeg_installed():
                    from .processor.ffmpeg import ffmpeg_concat_ts_to_mkv
                    ffmpeg_concat_ts_to_mkv(parts, output_filepath)
                else:
                    from .processor.join_ts import concat_ts
                    concat_ts(parts, output_filepath)
                print('Merged into %s' % output_filename)
            except:
                raise
            else:
                for part in parts:
                    os.remove(part)

        else:
            print("Can't merge %s files" % ext)

    print()


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
                tiktok_download('https://www.tiktok.com/share/video/' + id)
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
