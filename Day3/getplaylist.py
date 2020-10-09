# 引入 requests 模組
import requests as req
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
# 引入 re 模組
import re

def playlist_urls(url):  # 取得播放清單所有影片網址的自訂函式
    urls = []   # 播放清單網址
    if '&list=' not in url : return urls    # 單一影片
    response = req.get(url)    # 發送 GET 請求
    if response.status_code != 200:
        print('請求失敗')
        return
    #-----↓ 請求成功, 解析網頁 ↓------#
    soup = BeautifulSoup(response.text, 'lxml')
    a_list = soup.find_all('a')
    base = 'https://www.youtube.com/'    # Youtube 網址
    for a in a_list:
        href = a.get('href')
        url = base + href  # 主網址結合 href 才是完整的影片網址
        if ('&index=' in url) and (url not in urls):
            urls.append(url)
    return urls

playlist_link = 'https://www.youtube.com/watch?v=n7KpZoJy_j4&list=PLliocbKHJNwvnlL9xkwhdkaqmPbI9LU0m' #影片播放清單連結

urls = playlist_urls(playlist_link)   #執行 playlist_urls 函式

urls.sort(key = lambda s:int(re.search('index=\d+',s).group()[6:]))

for url in urls:
    print(url)
