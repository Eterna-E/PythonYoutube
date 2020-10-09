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
#設定網址輸入區域
input_frm = tk.Frame(win, width=640, height=50)
input_frm.pack()
#設定提示文字
lb = tk.Label(input_frm, text='Type a link like a video or a playlist',
             fg='black')
lb.place(rely=0.2, relx=0.5, anchor='center')
#設定輸入框
input_url = tk.StringVar()     # 取得輸入的網址
input_et = tk.Entry(input_frm, textvariable=input_url, width=60)
input_et.place(rely=0.75, relx=0.5, anchor='center')
#設定按鈕
#-----------------------------------------------------------------
def btn_click():   # 按鈕的函式
    print('後面再實作')
#-----------------------------------------------------------------
btn = tk.Button(input_frm, text='Download', command = btn_click,
                bg='orange', fg='Black')
btn.place(rely=0.75, relx=0.9, anchor='center')


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