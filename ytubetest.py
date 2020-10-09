from PIL import Image,ImageTk
import tkinter as tk
#------------↓主視窗↓------------#
win = tk.Tk()                          # 建立主視窗物件
win.geometry('640x480')                # 設定主視窗預設尺寸為640x480
win.resizable(False,False)             # 設定主視窗寬、高皆不可縮放
win.title('YouTube Video Downloader')  # 主視窗標題
win.iconbitmap('YouTube.ico')
#------------↓ Label：顯示圖片 ↓------------#
img=Image.open("youtube.png")     #
img=ImageTk.PhotoImage(img)
imLabel=tk.Label(win,image=img)
imLabel.pack()
# #------------↓ Frame：網址輸入區域 ↓------------#
# input_fm = tk.Frame(win, width=640, height=50)# 建立 Frame
# input_fm.pack()
# #--↓Label↓--#
# lb = tk.Label(input_fm, text='Type a link like a video or a playlist',
#              fg='black',font=12)
# lb.place(rely=0.2, relx=0.5, anchor='center')
# #--↓Entry↓--#
# yt_url = tk.StringVar()     # 取得使用者輸入的網址
# entry = tk.Entry(input_fm, textvariable=yt_url, width=60)
# entry.place(rely=0.75, relx=0.5, anchor='center')
# #--↓Button↓--#
# def click_func():   # 按鈕的自訂函式
#     print('後面再實作')
# btn = tk.Button(input_fm, text='Download', command = click_func,
#                 bg='orange', fg='Black',font=10)
# btn.place(rely=0.75, relx=0.9, anchor='center')



# #------------↓ Frame：下方顯示下載清單區域 ↓------------#
# dload_fm = tk.Frame(win, width=640, height=280)
# dload_fm.pack()
# #--↓ Label ↓--#
# lb = tk.Label(dload_fm, text='Download list',
#               fg='black', font=10)
# lb.place(rely=0.1, relx=0.5, anchor='center')
# #--↓ Listbox ↓--#
# listbox = tk.Listbox(dload_fm, width=65, height=15)
# listbox.place(rely=0.6, relx=0.5, anchor='center')
# #--↓ Scrollbar ↓--#
# sbar = tk.Scrollbar(dload_fm)
# sbar.place(rely=0.6, relx=0.87, anchor='center', relheight=0.75)
# #--↓  List 與 Scrollbar 的連結 ↓--#
# listbox.config(yscrollcommand = sbar.set)
# sbar.config(command = listbox.yview)


#--↓啟動主視窗↓--#
win.mainloop()