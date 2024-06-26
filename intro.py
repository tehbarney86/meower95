from tkinter import *
import json

welcome_messages = ("Welcome to Meower95! Select your server:",
                    "Select a server by clicking it's title on the list below:",
                    "Just click a name below to continue.",
                    "Point your cursor to a server below and click.",
                    "Just do it.",
                    "Dude...",
                    "Stop trying! There's no easter egg, nor whatever.",
                    "Okay let me explain:",
                    "You use your mouse pointer (the thing you click with),",
                    "And point it directly to the server you need to chat.",
                    "Click, and then click me again.",
                    "No, you do the stuff I said first, then you click.",
                    "Okay, you're just annoying, stop trying to be funny.",
                    "Next time you click I'll crash the program.")
welcome_count = 0
intro_part = 0
server = None

def refresh():
    for i in ("welcome","servers","user_title","users"):
        eval(i+".place_forget()")
        eval(i+".forget()")
    welcome.place_forget()
    bback.configure(state=DISABLED if intro_part == 0 else NORMAL)
    bnext.configure(text="Chat!" if intro_part else "Next")
    if intro_part:
        user_title.place(x=5,y=5)
        users.place(x=5,y=30,width=310,height=135)
    else:
        welcome.place(x=5,y=5)
        servers.place(x=5,y=30,width=310,height=135)
    users.delete(0,END)
    try:
        for i in list(cfg["servers"][server]["logins"].keys()):
            users.insert(END,i)
    except KeyError: pass
def next():
    global welcome_count,server,intro_part
    if intro_part == 0: #replace with case, no documentation offline yk
        try:
            server = servers.selection_get()
        except TclError:
            welcome_count += 1
            return
    intro_part += 1
    refresh()
def back():
    global intro_part
    if intro_part > 0: intro_part -= 1
    refresh()

cf = open("meower95.conf","r")
cfg = json.load(cf)
cf.close()

intro = Tk()
intro.geometry("320x200")
intro.title("Meower95 - Quick login")

welcome = Label(intro, font=("Helvetica", 10))
servers = Listbox(intro, font=("Helvetica", 10))
user_title = Label(intro, text="Select your user account:", font=("Helvetica", 10))
users = Listbox(intro, font=("Helvetica", 10))
bback = Button(intro, text="Back",command=back,font=("Helvetica", 10),state=DISABLED)
bnext = Button(intro, text="Next",command=next,font=("Helvetica", 10))
badd = Button(intro, text="Add...",font=("Helvetica", 10))

bback.place(x=5,y=198,anchor="sw")
bnext.place(x=315,y=198,anchor="se")
badd.place(x=160,y=198,anchor="s")

for i in list(cfg["servers"].keys()):
    servers.insert(END,i)

refresh()

try:
    while intro.wm_state() == "normal" and intro_part < 2:
        intro.update()
        welcome.configure(text=welcome_messages[welcome_count])
    intro.quit()
    intro.destroy()
except TclError:
    pass
