import tkinter as tk
from tkinter import ttk
def callbackFunc(event):
     print("Selected "+comboExample.get())

app = tk.Tk()
app.geometry('200x100')

labelTop = tk.Label(app,
                    text = "Choose your favourite month")
labelTop.grid(column=0, row=0)

comboExample = ttk.Combobox(app,
                            values=[
                                    "default",
                                    "January",
                                    "February",
                                    "March",
                                    "April"],state="readonly")

comboExample.grid(column=0, row=1)
comboExample.current(0)

comboExample.bind("<<ComboboxSelected>>", callbackFunc)

app.mainloop()
