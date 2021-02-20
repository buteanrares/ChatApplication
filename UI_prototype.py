import tkinter as tk

window = tk.Tk()

textBox = tk.Text(height=20,width=60)
textBox.place(x=1,y=1)

messageEntry = tk.Entry(width=20)
messageEntry.place(x=0,y=340)

sendButton = tk.Button(text="Send")
sendButton.place(x=160,y=340)

window.minsize(650,430)

window.mainloop()