from PIL import Image,ImageTk
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube
import threading
import time
#-----------------------------------------------------------------
import os
import subprocess
# 引入 requests 模組
import requests as req
# 引入 Beautiful Soup 模組
from bs4 import BeautifulSoup
# 引入 re 模組
import re
# import pyautogui
from tkinter import ttk
#-----------------------------------------------------------------

fileobj = {}
download_count = 1

#--------------------函式區域----------------------------------------------
# 檢查影片檔是否包含聲音
def check_media(filename):
    r = subprocess.Popen(["ffprobe", filename],
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = r.communicate()

    if (out.decode('utf-8').find('Audio') == -1):
        return -1  # 沒有聲音
    else:
        return 1

# 合併影片檔
def merge_media():
    temp_video = os.path.join(fileobj['dir'], 'temp_video.mp4')
    temp_audio = os.path.join(fileobj['dir'], 'temp_audio.mp4')
    temp_output = os.path.join(fileobj['dir'], 'output.mp4')

    cmd = f'"ffmpeg" -i "{temp_video}" -i "{temp_audio}" \
        -map 0:v -map 1:a -c copy -y "{temp_output}"'
    try:
        subprocess.call(cmd, shell=True)
        # 視訊檔重新命名
        os.rename(temp_output, os.path.join(fileobj['dir'], fileobj['name']))
        os.remove(temp_audio)
        os.remove(temp_video)
        print('視訊和聲音合併完成')
        # fileobj = {}
    except:
        print('視訊和聲音合併失敗')

def onProgress(stream, chunk, remains):
    total = stream.filesize
    percent = (total-remains) / total * 100
    print('下載中… {:05.2f}%'.format(percent), end='\r')

def download_sound():
    try:
        yt.streams.filter(type="audio").first().download()
    except:
        print('下載影片時發生錯誤，請確認網路連線和YouTube網址無誤。')
        return

# 檔案下載的回呼函式
def onComplete(stream, file_path):
    global download_count, fileobj
    fileobj['name'] = os.path.basename(file_path)
    fileobj['dir'] = os.path.dirname(file_path)
    print('\r')

    if download_count == 1:
        if check_media(file_path) == -1:
            print('此影片沒有聲音')
            download_count += 1
            try:
                # 視訊檔重新命名
                os.rename(file_path, os.path.join(
                    fileobj['dir'], 'temp_video.mp4'))
            except:
                print('視訊檔重新命名失敗')
                return

            print('準備下載聲音檔')
            download_sound()          # 下載聲音
        else:
            print('此影片有聲音，下載完畢！')
    else:
        try:
            # 聲音檔重新命名
            os.rename(file_path, os.path.join(
                fileobj['dir'], 'temp_audio.mp4'))
        except:
            print("聲音檔重新命名失敗")
        # 合併聲音檔
        merge_media()

def links_get(url):  # 取得播放清單所有影片網址的自訂函式
    urls = []   # 播放清單網址
    if '&list=' not in url :
        return urls    # 單一影片
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

lock = threading.Lock()

def video_download(url, listbox,name,video_path,itag):
    download_count = 1 #改回1
    print(url) #印出影片網址
    global yt
    yt = YouTube(url, on_progress_callback=onProgress,on_complete_callback=onComplete)
    # name = yt.title
    time.sleep(0.01)
    lock.acquire()              # 進行鎖定
    no = listbox.size()     # 以目前列表框筆數為下載編號
    listbox.insert(tk.END, f'{no:02d}:{name}.....下載中')
    print('插入:', no, name)
    lock.release()              # 釋放鎖定
    try:
        if itag == '' or itag=='default':
            os.system('you-get '+' -o '+ "\"" +video_path+ "\""+" "+"\""+ url + "\"")
        if itag != '':
            os.system('you-get '+'--itag='+itag+' -o '+ "\"" +video_path+ "\""+" "+"\""+ url + "\"")
    except:
        try:
            print(yt.streams.filter(subtype='mp4',resolution="1080p")[0].download())
        except:
            print(yt.streams.filter(subtype='mp4',resolution="1080p")[1].download())
    lock.acquire()              # 進行鎖定
    print('更新:', no, name)
    listbox.delete(no)
    listbox.insert(no, f'{no:02d}:●{name}.....下載完成')
    lock.release()              # 釋放鎖定
    # print(fileobj)
    return

def yget_quality(url,video_quality):
    if video_quality=='default quality':
        return 'default'
    process = subprocess.Popen('you-get -i ' + url,
                       shell=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
#-------------------------------------------------------------------------
#------------↓主視窗↓------------#
win = tk.Tk()                          # 建立主視窗物件
win.geometry('640x600')                # 設定主視窗預設尺寸為640x480
win.resizable(False,False)             # 設定主視窗寬、高皆不可縮放
win.title('YouTube Video Downloader')  # 主視窗標題
win.iconbitmap('YouTube.ico')
#------------↓ Label：顯示圖片 ↓------------#
img=Image.open("youtube.png")     #
img=ImageTk.PhotoImage(img)
imLabel=tk.Label(win,image=img)
imLabel.pack()
#設定網址輸入區域
input_frm = tk.Frame(win, width=640, height=50)
input_frm.pack()
#設定提示文字
lb = tk.Label(input_frm, text='Type a link like a video or a playlist',
             fg='black')
lb.place(rely=0.2, relx=0.5, anchor='center')
#設定提示文字
lb = tk.Label(input_frm, text='link :',
             fg='black')
lb.place(rely=0.5, relx=0.1)
#設定輸入框
input_url = tk.StringVar()     # 取得輸入的網址
input_et = tk.Entry(input_frm, textvariable=input_url, width=60)
input_et.place(rely=0.75, relx=0.5, anchor='center')
#設定按鈕
#-----------------------------------------------------------------

def btn_click():   # 按鈕的函式
    listbox.delete(0,tk.END)

    url = input_url.get()          # 取得文字輸入框的網址
    try:    #  測試 pytube 是否支援此網址或者網址是否正確
        YouTube(url)
    except:
        messagebox.showerror('錯誤','pytube 不支援此影片或者網址錯誤')
        return
    #-----↓ 選擇下載品質 ↓------#
    video_itag = yget_quality(url,cbb.get())
    if video_itag=='':
        messagebox.showwarning('quality','video quality not support download default quality')
    #-----↓ 選擇下載路徑 ↓------#
    if var_path_text.get()=='':
        messagebox.showwarning('Download path','please choose a Download path')
        return
    #-----↓ 此 pytube 支援此網址, 進行網路爬蟲 ↓------#
    urls = links_get(url)
    #------------↓ 輸入網址中有影片清單 ↓-----------------#
    if urls and messagebox.askyesno('確認方塊',
            '是否下載清單內所有影片？(選擇 否(N) 則下載單一影片)') :
    #--------↓ 下載清單中所有影片 ↓---------#
        # pyautogui.press('enter')
        print('開始下載清單')
        listbox.insert(tk.END, '.....開始下載清單.....')
        urls.sort(key = lambda s:int(re.search("index=\d+",s).group()[6:]))#對所有影片網址做排序
        ytname = []
        for i in range(len(urls)):
            yt_title = YouTube(urls[i]).title
            time.sleep(0.2)
            print('title',yt_title)
            ytname.append(yt_title)
        # for url in urls:     # 建立與啟動執行緒
        for i in range(len(urls)):
            time.sleep(0.5)
            threading.Thread(target = video_download,
                             args=(urls[i], listbox, ytname[i], var_path_text.get(), video_itag)).start()
            # video_download(url, listbox)
    #--------↓ 下載單一影片 ↓---------#
    else:
        yt = YouTube(url)
        if messagebox.askyesno('確認方塊',
                               f'是否下載{yt.title}影片？') :
            threading.Thread(target = video_download,
                             args=(url, listbox, yt.title, var_path_text.get(), video_itag)).start()
            # video_download(url, listbox)
        else:
            print('取消下載')

#-----------------------------------------------------------------
btn = tk.Button(input_frm, text='Download', command = btn_click,
                bg='orange', fg='Black')
btn.place(rely=0.75, relx=0.9, anchor='center')



#-----------------------------------------------------------------
#選擇區域：解析度下拉選單和影片下載路徑選擇
choice_frm = tk.Frame(win, width=640, height=50)
choice_frm.pack()
#設定提示文字
lb = tk.Label(choice_frm, text='choose video quality :',
             fg='black')
lb.place(rely=0.2,relx=0.1)
#解析度下拉選單
def callbackFunc(event):
     print("Selected "+cbb.get())

cbb = ttk.Combobox(choice_frm,
                            values=[
                                    "default quality",
                                    "1080p",
                                    "720p",
                                    "480p",
                                    "360p"],state="readonly",width=12)

cbb.place(rely=0.2,relx=0.3)
cbb.current(0)
# print(cbb.get())
cbb.bind("<<ComboboxSelected>>", callbackFunc)
#影片下載路徑選擇
from tkinter.filedialog import askdirectory
def select_path():
    path_ = askdirectory()
    var_path_text.set(path_)

label_path = tk.Label(choice_frm, text='Download path :', cursor='xterm')
label_path.place(rely=0.2,relx=0.5)
var_path_text = tk.StringVar()
entry_path = tk.Entry(choice_frm, fg='gray', bd=2, width=20, textvariable=var_path_text, cursor='xterm')
entry_path.place(rely=0.2,relx=0.66)
button_choice = tk.Button(choice_frm, text='change', bd=1, width=6, command=select_path, cursor='hand2')
button_choice.place(rely=0.15,relx=0.9)

#-----------------------------------------------------------------


#下載清單區域
dl_frm = tk.Frame(win, width=640, height=280)
dl_frm.pack()
#設定提示文字
lb = tk.Label(dl_frm, text='Download list',
              fg='black')
lb.place(rely=0.1, relx=0.5, anchor='center')
#設定顯示清單
listbox = tk.Listbox(dl_frm, width=65, height=15)
listbox.place(rely=0.6, relx=0.5, anchor='center')
#設定捲軸
sbar = tk.Scrollbar(dl_frm)
sbar.place(rely=0.6, relx=0.87, anchor='center', relheight=0.75)
#連結清單和捲軸
listbox.config(yscrollcommand = sbar.set)
sbar.config(command = listbox.yview)

#啟動主視窗
win.mainloop()