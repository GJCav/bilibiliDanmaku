# 此项目已被废弃
B站API已经大变样了，这个项目还停留在5年前，做个留恋吧。 

# 用于下载Bilibili的弹幕
> 我看过很多相似的代码，但都只能下载www.bilibili.com/video/avXXXXX的弹幕，
> 不能下载bangumi.bilibili.com/anime/XXXXXX下的弹幕，并且对于弹幕文件`XXXX.xml`中
> <d p="XXXX">的p属性中的参数没有进行解析，此项目就是为了解决这些问题。

## Feature
1. 下载bangumi.bilibili.com/anime/下的弹幕
2. 下载www.bilibili.com/video/avXXXXX下的弹幕
3. 解析弹幕文件，并赋予p属性中的参数意义

## Document
1. danmaku.py

有函数：danmaku, danmakuParser

danmaku负责下载弹幕xml文件，danmakuParser负责解析xml文件，使之便于阅读

## Example
URL: https://www.bilibili.com/video/av13203221/

Code:
<pre>
from danmaku import *
from pprint import pprint

url = "https://www.bilibili.com/video/av13203221/"
pprint(danmakuParser(danmaku(url)))
</pre>

Output:
<pre>
[{'color': '0xffffff',
  'danmuid': '3677664588',
  'date': '2017-08-10 21:23:50',
  'fontsize': 25,
  'msg': '陆上最强',
  'pool': '0',
  'time': 396.64898681641,
  'timestamp': 1502371430,
  'type': 1,
  'userid': '458b4187'},
 {'color': '0xffffff',
  'danmuid': '3677665426',
  'date': '2017-08-10 21:24:00',
  'fontsize': 25,
  'msg': '夹击妹抖',
  'pool': '0',
  'time': 442.30899047852,
  'timestamp': 1502371440,
  'type': 1,
  'userid': '5ca6b303'},
.....
</pre>

## 关于弹幕xml文件的解释
文件结构如下
<pre>
&lt;i&gt;
&lt;chatserver&gt;chat.bilibili.com&lt;/chatserver&gt;
&lt;chatid&gt;21651589&lt;/chatid&gt;
&lt;mission&gt;0&lt;/mission&gt;
&lt;maxlimit&gt;1500&lt;/maxlimit&gt;
&lt;source&gt;k-v&lt;/source&gt;
%3Cd p=&quot;180.57899475098,1,25,16777215,1502371152,0,5ca6b303,3677640812&quot;&gt;社长&lt;/d%3E
&lt;d p=&quot;775.22601318359,1,25,0,1502371182,0,efc9d749,3677643202&quot;&gt;好好好好！！！&lt;/d&gt;
&lt;d p=&quot;131.26400756836,1,25,16777215,1502371211,0,bd56ada8,3677645814&quot;&gt;好的抱走临。。。（woc别拿小刀扎我&lt;/d&gt;
&lt;d p=&quot;645.63598632812,1,25,16777215,1502371239,0,d28087eb,3677648118&quot;&gt;团长好魔性的笑声&lt;/d&gt;
</pre>
解释如下
<pre>
&lt;d p="time, type, fontsize, color, timestamp, pool??, userID, danmuID"&gt;
        0     1     2          3     4     5       6         7
type:
	1: up   scroll
	2: advantage danmu(not test yet)
	3: advantage danmu(not test yet)
	4: down static
	5: up   static
</pre>
time-弹幕在视频中的播放时间<br/>
type-弹幕类型解释中有<br/>
fontsize-是个人就看得懂<br/>
color-十六进制的颜色信息转成十进制的值<br/>
timestamp-弹幕发送时的timestamp<br/>
pool-我也不知道，但发送弹幕的数据包post了这个值<br/>
userID-与在个人中心那的uid不同，但也是用户的唯一id
danmuID-弹幕的唯一id，用于管理（撤回）弹幕
