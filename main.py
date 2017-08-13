from danmaku import *
from pprint import pprint
from sys import argv


if __name__ == '__main__':
    saveFile = '1.xml'
    url = "https://www.bilibili.com/video/av13203221/"
    pprint(danmakuParser(danmaku(url)))