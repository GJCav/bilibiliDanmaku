import re as Regex
import requests as Request
import json as Json
import xml.etree.cElementTree as ET
import time as Time

__all__ = ['danmaku', 'danmakuParser']
# def getCookies():
#     jsonStr = '';
#     with open('bilibili.cookie', encoding='utf-8') as file:
#         jsonStr = file.read()
#     json = Json.loads(jsonStr, encoding='utf-8')
#     global cookies
#     for obj in json:
#         cookies[obj['name']] = obj['value']
# getCookies()

bilibiliHeaders = {
    'user-agent': 'fiddler',
    'host': 'www.bilibili.com',
    'accept-encoding': 'gzip, deflate, sdch'
}

bangumiHeaders = {
    'user-agent': 'fiddler',
    'host': 'bangumi.bilibili.com',
    'accept-encoding': 'gzip, deflate, sdch'
}

danmakuHeaders = {
    'host':'comment.bilibili.com',
    'user-agent':'fiddler',
    'origin':'https://www.bilibili.com',
    'accept-encoding':'gzip, deflate, sdch'
}


def downloadDanmaku(cid:str) -> str:
    """
    Download danmaku from cid
    :param cid: str
    :return: str
    """
    url = 'https://comment.bilibili.com/%s.xml' % cid
    r = Request.get(url, headers=danmakuHeaders)
    return r.text


def fromBilibiliWebsite(url:str, cookies:dict = {}) -> str:
    """
    Search cid from urls like "https://www.bilibili.com/video/"
    :param url: str
    :return: str
    """
    r = Request.get(url, headers = bilibiliHeaders, cookies=cookies)
    if not r.status_code == 200:
        return None

    groups = Regex.findall(r'.+?#page=(\d+)', url)
    if not groups:
        result = Regex.findall(r'cid=(.+?)&aid=', r.text)
        if result:
            return downloadDanmaku(result[0])
    else:
        page = int(groups[0])
        groups = Regex.findall(r'cid=(.+?)&aid=', r.text)
        if groups:
            firstPageCid = int(groups[0])
            curPageCid = str(firstPageCid + page - 1)
            return downloadDanmaku(curPageCid)


def fromBangumiWebsite(url:str, cookies:dict = {}) -> str:
    """
    Search cid from urls like "https://bangumi.bilibili.com/anime/{id}/play#{eid}".
    :param url:
    :return: str
    """
    result = Regex.findall(r'play#(.+)', url)
    if not result:
        return None

    eid = result[0]
    infurl = 'https://bangumi.bilibili.com/web_api/episode/%s.json' % eid
    r = Request.get(infurl, headers=bangumiHeaders, cookies=cookies)

    json = Json.loads(r.text)
    cid = json['result']['currentEpisode']['danmaku']

    return downloadDanmaku(cid)


def danmaku(url:str, cookies:dict = {}) -> str:
    """
    Download danmaku by giving url according to video you want.
    This method will return str in xml format
    :param url:
    :return: str
    """
    if url.find('//bangumi.bilibili.com/') != -1:
        return fromBangumiWebsite(url, cookies)
    elif url.find('//www.bilibili.com/') != -1:
        return fromBilibiliWebsite(url, cookies)


def danmakuParser(xml:str) -> list:
    """
    Parse xml from method `danmaku`.
    The map in the returned list will contain keys,
    which are "msg", "type", "fontsize", "color",
    "date", "rawdate","pool", "userid" and "danmakuid" .

    Especially, "userid" is special.
    :param xml: str
    :return: list
    """
    tree = ET.fromstringlist(xml)
    danmakulist = []
    for tag in tree:
        if tag.tag == 'd':
            info = {}

            info['msg'] = tag.text

            params = tag.get('p').split(',')
            info['time'] = float(params[0])
            info['type'] = int(params[1])
            info['fontsize'] = int(params[2])
            info['color'] = hex(int(params[3]))
            info['date'] = Time.strftime(
                '%Y-%m-%d %H:%M:%S',
                Time.localtime(
                    int(params[4])
                )
            )
            info['timestamp'] = int(params[4])
            info['pool'] = params[5]
            info['userid'] = params[6]
            info['danmuid'] = params[7]

            danmakulist.append(info)
    return danmakulist


if __name__ == '__main__':
    pass