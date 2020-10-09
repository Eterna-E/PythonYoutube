import subprocess as sp  # 更名為較簡短的 sp
import os

def yget_info(url):
    process = sp.Popen('you-get -i ' + url,
                       shell=True,
                       stdout=sp.PIPE, stderr=sp.PIPE)
    r = process.communicate()
    s = str(r[0], 'utf-8')
    if s.find('title:') < 0:  # 搜不到 title: 則視為失敗
        return '', ''
    title = s[s.find('title:')+6: s.find('streams')].strip()
    itag  = s[s.find('itag:')+6: s.find('container')].strip()
    if len(itag) > 8:   #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
        itag = itag[4:-4]  #去除、前後4個 ESC 字元
    return title, itag  #↑傳回 title 為空字串時表示讀取失敗

#--------↓ you-get 下載影片自訂函式 ↓---------#
def yget_dl(url, itag = None):
    cmd = 'you-get '
    if itag:
        cmd = cmd + '--itag=' + itag + ' '
    os.system(cmd + url)
    # process = sp.Popen(cmd + url)
    # process.wait()
    return 0 #process.returncode  #傳回 0 表 OK

def yget_quality(url,video_quality):
    process = sp.Popen('you-get -i ' + url,
                       shell=True,
                       stdout=sp.PIPE, stderr=sp.PIPE)
    r = process.communicate()
    s = str(r[0], 'utf-8')
    print(s)
    if s.find('title:') < 0:  # 搜不到 title: 則視為失敗
        print('影片資訊讀取失敗')
    # title = s[s.find('title:')+6: s.find('streams')].strip()
    # print(title)
    #限定Full HD 1080p
    fhdq_s = s[s.find('1920x1080')-80:s.rfind('1920x1080')+115].rstrip()
    #限定Full HD 1080p mp4 格式
    fhdq_mp4 = fhdq_s[fhdq_s.find('mp4')-50:fhdq_s.find('mp4')+135]
    # print(fhdq_mp4)
    fhdq_itag = fhdq_mp4[fhdq_mp4.find('itag:')+6: fhdq_mp4.find('container')].strip()
    # print(fhdq_itag)
    if len(fhdq_itag) > 8:   #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
        fhdq_itag = fhdq_itag[4:-4]  #去除、前後4個 ESC 字元
    if video_quality=='1080p':
        return fhdq_itag

    #限定HD 720p
    hdq_s = s[s.find('1280x720')-80:s.rfind('1280x720')+115].rstrip()
    #限定HD 720p mp4 格式
    hdq_mp4 = hdq_s[hdq_s.find('mp4')-50:hdq_s.find('mp4')+135]
    # print(hdq_mp4)
    hdq_itag = hdq_mp4[hdq_mp4.find('itag:')+6: hdq_mp4.find('container')].strip()
    # print(hdq_itag)
    if len(hdq_itag) > 8:   #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
        hdq_itag = hdq_itag[4:-4]  #去除、前後4個 ESC 字元
    if video_quality=='720p':
        return hdq_itag

    #限定 middle quality 480p
    mq_s = s[s.find('854x480')-80:s.rfind('854x480')+115].rstrip()
    #限定 middle quality 480p mp4 格式
    mq_mp4 = mq_s[mq_s.find('mp4')-50:mq_s.find('mp4')+135]
    # print(mq_mp4)
    mq_itag = mq_mp4[mq_mp4.find('itag:')+6: mq_mp4.find('container')].strip()
    # print(mq_itag)
    if len(mq_itag) > 8:   #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
        mq_itag = mq_itag[4:-4]  #去除、前後4個 ESC 字元
    if video_quality=='480p':
        return mq_itag

    #限定 low quality 360p
    lq_s = s[s.find('640x360')-80:s.rfind('640x360')+115].rstrip()
    #限定 low quality 360p mp4 格式
    lq_mp4 = lq_s[lq_s.find('mp4')-50:lq_s.find('mp4')+135]
    # print(lq_mp4)
    lq_itag = lq_mp4[lq_mp4.find('itag:')+6: lq_mp4.find('container')].strip()
    # print(lq_itag)
    if len(lq_itag) > 8:   #如果 itag0 內容有 ESC 資料(例 b'\x1b[7m137\x1b[0m')
        lq_itag = lq_itag[4:-4]  #去除、前後4個 ESC 字元
    if video_quality=='360p':
        return lq_itag

#--------↓ you-get 下載影片主程式 ↓---------#
# url = 'https://www.youtube.com/watch?v=n7KpZoJy_j4'  # 影片網址
# title, best = yget_info(url)	# 取得名稱與 itag
# print(title, best)
# r = yget_dl(url, best)	# 高品質下載
# print('下載高品質:', 'OK' if r==0 else 'Error')  #傳回 0 表 OK
# r = yget_dl(url)		# 預設品質下載
# print('下載一般品質:', 'OK' if r==0 else 'Error')

# yget_quality('https://www.youtube.com/watch?v=hOsLhprhIOw')
if yget_quality("https://www.youtube.com/watch?v=n7KpZoJy_j4&list=PLliocbKHJNwvnlL9xkwhdkaqmPbI9LU0m&t=1s",'720p')=='':
    print('不支援')
# yget_quality('https://www.youtube.com/watch?v=wdH26D8Ssww')
print(yget_quality("https://www.youtube.com/watch?v=n7KpZoJy_j4&list=PLliocbKHJNwvnlL9xkwhdkaqmPbI9LU0m&t=1s",'360p'))