import tkinter as tk

window = tk.Tk()

textBox = tk.Text(height=20,width=60)
textBox.place(x=1,y=1)

messageLabel = tk.Label()
messageLabel.place(x=0,y=340)

messageEntry = tk.Entry(width=20)
messageEntry.place(x=0,y=360)

sendButton = tk.Button(text="Send")
sendButton.place(x=160,y=360)

window.minsize(650,460)

window.mainloop()