
import pyautogui
import time
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import os
from tkinter import scrolledtext as st
import notify2
import subprocess
from tkinter import *
from tkinter import ttk
import tkinter as tk
from threading import Thread
import keyboard
import speech_recognition as sr
import pyaudio
import pocketsphinx



root = tk.Tk()
root.title("Easyread 1.0") # title
#root.resizable(0, 0) # if you want it resizeable, just remove this whole line

scrollLength_sv = tk.StringVar()
time_sv = tk.StringVar()
scrollInterval_sv = tk.StringVar()

class easyRead:
    def scrollPage(self):
        try:
           # print("\nBefore using this feature, it's advised you minimize all unwanted windows,\nleaving only the one you want to scroll on. \nYou'd have 10 seconds to do this after providing all parameters.\n")
            #time.sleep(1)
            scrollLength = scrollLength_sv.get(); scrollLength = int(scrollLength)
            delayString = scrollInterval_sv.get()
            if len(delayString) == 10:
                delayInt = delayString[0:2]; delayInt = int(delayInt)
            elif len(delayString) < 10:
                delayInt = delayString[0]; delayInt = int(delayInt)
            time.sleep(1)
            pyautogui.click(698, 357)
            time.sleep(1)
            while True:
                pyautogui.scroll(scrollLength)
                time.sleep(delayInt)
        except KeyboardInterrupt:
            print("\nDone")
        except pyautogui.FailSafeException:
            print('\nDone.\n')

    def createMenu(self, *event): # App Menu 
        menubar = tk.Menu(root)
        root.config(menu=menubar)

        settingsMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=settingsMenu)
        settingsMenu.add_command(label="Load PDF", command=self.loadPdf)
        settingsMenu.add_command(label="About", command=self.about)
        settingsMenu.add_separator()
        settingsMenu.add_command(label="Exit", command=self.exitWindow)

        helpMenu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="Tutorial", command=self.helpTutorial)
        


    def loadPdf(*event):
        
        path = fd.askopenfilename()

        if path == "":
            return
        #basename = "/"+ os.path.basename(path)
        
        fname, fext = os.path.splitext(path)

        if fext != ".pdf":
            mb.showerror("Wrong extension!", "This is a wrong extension!\nJust *.txt, pdf, docx allowed!")
        else:
            subprocess.call(["xdg-open",path])
            time.sleep(2)
            easyread.sendStartNotification()           
            easyread.callback()
            #t1 = Thread(target=easyread.triggerScroll)
            #t1.start() #Calls first function

            #easyread.sendTimeNotification()
            
    def callback(self):
        r = sr.Recognizer()
        m = sr.Microphone()
        with sr.Microphone() as source:
            with m as source:
                time.sleep(4)
                r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

            try:
                while True:
        
                    print("Say something!")
                    with m as source: audio = r.listen(source)
                    print("Got it! Now to recognize it...")
                    try:
                        print("Sphinx thinks you said " + r.recognize_sphinx(audio))
                        if r.recognize_sphinx(audio) == "okay":
                            easyread.scrollPage()
                        elif r.recognize_sphinx(audio) != "okay":
                            easyread.sendErrorNotification()
                    except sr.UnknownValueError:
                        print("Sphinx could not understand audio")
                    except sr.RequestError as e:
                        print("Sphinx error; {0}".format(e))
            except KeyboardInterrupt:

                print("No longer listening")


    
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    #self.stop_listening = r.listen_in_background(self, m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    def exitWindow(self, *event):
        root.destroy()

    def helpTutorial(self,*event):
        rootHelp = tk.Tk()
        rootHelp.title("How To Use")
        rootHelp.geometry("528x297")
        rootHelp.resizable(0, 0)

        helpText = "yhjkhjgkhjyhfgjhkjhfhgkjfhgfkjg"
        paper = st.ScrolledText(rootHelp, width=400, height=200, font=("Consolas", 8))
        paper.insert("1.0", helpText)
        paper.configure(state='disabled')
        paper.pack()

    def about(self, *event):
        rootDocumentary = tk.Tk()
        rootDocumentary.title("About EasyRead")
        rootDocumentary.geometry("538x297")
        rootDocumentary.resizable(0, 0)

        documentaryText = "EasyRead is a PDF reading assistant that helps users study with ease, cancelling  out the traditional stress of having to mannually scroll a page anytime a user wants to scroll.\nEasyRead as a project was started by Onyenanu Princewill, but has now been made open source to get others to contribute.\nConnect with me via twitter: @iam_princek\nvia email: princekelvin91@gmail.com"

        paper = st.ScrolledText(rootDocumentary, width=400, height=200, font=("Consolas", 8))
        paper.insert("1.0", documentaryText)
        paper.configure(state='disabled')
        paper.pack()

        rootDocumentary.mainloop()

    def sendStartNotification(self):
        notify2.init("EasyRead")
        notification = notify2.Notification("EasyRead 1.0", "App is listening\nSay 'okay' to trigger auto scroll", "notificar=tion-message-im")
        notification.show()
        # set timeout for a notification
        
    def sendErrorNotification(self):
    
        notify2.init("EasyRead")
        notification = notify2.Notification("EasyRead 1.0", "Invalid Command!\nSay 'okay' to trigger auto scroll", "notificar=tion-message-im")
        notification.show()
        
        # set timeout for a notification
        notification.set_timeout(50000)



    def getScrollLength(self, scrollLength_sv):
       return scrollLength_sv

    def getScrollInterval(self, scrollInterval_sv):
       return scrollInterval_sv
    
    
    timeChosenlabel = tk.Label(root, text="Estimated Study Time: ").grid(row=1, column=0, padx=10, pady=10, sticky='w')
    timeChosen = ttk.Combobox( width=15, textvariable=time_sv) #3
    timeChosen['values'] = ("5 minutes", "10 minutes", "15 minutes", "30 minutes", "1 hour")     # 4
    timeChosen.grid(column=1, row=1, padx=10)              # 5
    timeChosen.current(0)

    #later

    chooseButton = tk.Button(root, text="Load PDF", command=loadPdf).grid(row=4, column=1, padx=1, pady=10, sticky='w')
    
    
    ttk.Label( text="Choose a Scroll Length:").grid(column=0, row=2, padx=10)                         # 2
    numberChosen = ttk.Combobox( width=15, textvariable=scrollLength_sv) #3
    numberChosen['values'] = (-3, -5, -10, 1, 5, 10)     # 4
    numberChosen.grid(column=0, row=3, padx=10)              # 5
    numberChosen.current(0)

    #2nd dropdown
    ttk.Label( text="Choose Scroll Interval:").grid(column=1, row=2, padx=10)                        # 2
    intervalChosen = ttk.Combobox( width=15, textvariable=scrollInterval_sv) #3
    intervalChosen['values'] = ("5 seconds", "10 seconds", "15 seconds", "30 seconds", "1 minute")     # 4
    intervalChosen.grid(column=1, row=3, padx=10)              # 5
    intervalChosen.current(0)  
# bind and build
easyread = easyRead()
easyread.createMenu()        
root.mainloop()

