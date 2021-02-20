import tkinter as tk

window = tk.Tk()
window.columnconfigure(0, minsize=250)
window.rowconfigure([0, 1], minsize=100)

textBox = tk.Text(height=150,width=60)
textBox.place(x=1,y=1)

messageEntry = tk.Entry(width=20)
messageEntry.place(x=31,y=64)
messageEntry.grid(row=0,column=0,sticky="sw")

sendButton = tk.Button(text="Send")
sendButton.place(x=160,y=79)



window.mainloop()