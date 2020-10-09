import threading
import time

# 子執行緒要執行的函式
def print_num():
  for i in range(0,6):
    print("子執行緒:", i)
    time.sleep(1)

# 建立子執行緒物件
td = threading.Thread(target = print_num)

# 起動子執行緒
td.start()

# 主執行緒繼續執行
for i in range(3):
  print("主執行緒:", i)
  time.sleep(1)

# 等待 t 這個子執行緒結束
td.join()

print("執行結束")