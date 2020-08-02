from tkinter import *

def calc(event):
    label.config(text='Result : ' + str(eval(entry.get())))

root = Tk()
root.title('Stock')
root.geometry("840x600+100+100")
root.resizable(False, False)



# text box
txt = Entry(root, width=10)
txt.insert(0, 'stock code')
txt.place(x=0, y=10)
txt.pack()

# get text data
def btncmd():
    print(txt.get())
    stock_code = txt.get()
    listbox.insert(END, stock_code)
    txt.delete(0, END)

# button
btn1 = Button(root, text="Send", command=btncmd)
# button1.place(x=50, y=10)
btn1.pack()


#ListBox
listbox =Listbox(root, selectmode="extended", height=0)

listbox.pack()

root.mainloop()