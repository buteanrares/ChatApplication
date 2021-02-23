import tkinter as tk

window = tk.Tk()

textBox = tk.Text(height=20,width=60)
textBox.place(x=1,y=1)

messageLabel = tk.Label(text="Message:")
messageLabel.place(x=0,y=340)

messageEntry = tk.Entry(width=35)
messageEntry.place(x=0,y=360)

sendButton = tk.Button(text="Send", command=sendText)
sendButton.place(x=225,y=360)

microphoneButton = tk.Button(image=,command=toggleMicrophone)
microphoneButton.place(x=5,y=375)

headphoneButton = tk.Button(image=,command=toggleHeadphone)

window.minsize(650,400)

window.mainloop()

def sendText(text):
    # TODO
    pass

def toggleMicrophone():
    # TODO
    pass

def toggleHeadphone():
    # TOOD
    pass