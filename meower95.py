def log(*args,sep=" ",safe=False):
    if not exists("meower95.log"):
        lf = open("meower95.log","w")
        lf.write('''!!! WARNING !!!
Please do not share this file to anybody you don't know or trust.
This file can contain valuable information like your Meower
account passwords, tokens and etc. that can be used for malicious
intent by databrokers and trouble makers.
If you still need help online, share the contents of the file
meower95.safelog, as it contains only the important problems you
might face while using the program.

Thank you, barney86.

;3

''')
        lf.close()
    lf = open("meower95.log","a")
    t = time.gmtime()
    logput = f"{t[0]}.{t[1]}.{t[2]} {t[3]}:{t[4]}:{t[5]}: " + sep.join(args)
    lf.write(logput)
    lf.close()
    if safe:
        lf = open("meower95.safelog","a" if exists("meower95.safelog") else "w")
        lf.write(logput)
        lf.close()

import urllib.request, json, multiprocessing, os, time
from tkinter import *
from tkinter import ttk
from os.path import exists
from subprocess import call
from urllib.request import ssl
from urllib.error import URLError

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
server = user = None

def refresh_intro():
    users.delete(0,END)
    servers.delete(0,END)
    for i in ("welcome","servers","user_title","users"):
        eval(i+".place_forget()")
    welcome.place_forget()
    bback.configure(state=DISABLED if intro_part == 0 else NORMAL)
    bnext.configure(text="Chat!" if intro_part else "Next >")
    if intro_part:
        for i in list(cfg["servers"][server]["logins"].keys()):
            users.insert(END,i)
        user_title.place(x=130,y=5)
        users.place(x=130,y=30,width=310,height=135)
    else:
        for i in list(cfg["servers"].keys()):
            servers.insert(END,i)
            
        welcome.place(x=130,y=5)
        servers.place(x=130,y=30,width=310,height=135)
    
def next():
    global welcome_count,server,user,intro_part
    if intro_part: #replace with case, no documentation offline yk
        try:
            user = users.selection_get()
        except TclError:
            return
    else: #replace with case, no documentation offline yk
        try:
            server = servers.selection_get()
        except TclError:
            welcome_count += 1
            return
    
    intro_part += 1
    refresh_intro()

def back():
    global intro_part
    if intro_part > 0: intro_part -= 1
    refresh_intro()

def add():
    global cfg
    def save_cfg():
        global cfg
        if intro_part: cfg["servers"][server]["logins"][entry1.get()] = entry2.get()
        else:
            cfg["servers"][entry1.get()] = {}
            cfg["servers"][entry1.get()]["http"] = entry2.get()
            cfg["servers"][entry1.get()]["websocket"] = entry3.get()
            cfg["servers"][entry1.get()]["logins"] = {}
        cf = open("meower95.conf","w")
        json.dump(cfg,cf)
        cf.close()
        winadd.destroy()
        refresh_intro()
        
    winadd = Tk()
    winadd.title("Meower - Add " + ("user account" if intro_part else "server"))
    winadd.geometry("280x85" if intro_part else "280x105")
    
    Label(winadd,text="Username:" if intro_part else "Name:", font=("Helvetica", 8)).place(x=110,y=10,anchor="e")
    entry1 = Entry(winadd,font=("Helvetica", 8))
    entry1.place(x=110,y=10,width=165,anchor="w")
    Label(winadd,text="Password:" if intro_part else "HTTP(S) server:", font=("Helvetica", 8)).place(x=110,y=35,anchor="e")
    entry2 = Entry(winadd,font=("Helvetica", 8))
    if intro_part:
        entry2.configure(show="•")
        register = Button(winadd,text="Register account",font=("Helvetica", 8),state=DISABLED)
        register.place(x=140,y=85,anchor="s")
    else:
        Label(winadd,text="WS(S) server:", font=("Helvetica", 8)).place(x=110,y=60,anchor="e")
        entry3 = Entry(winadd,font=("Helvetica", 8))
        entry3.place(x=110,y=60,width=165,anchor="w")
    entry2.place(x=110,y=35,width=165,anchor="w")
    cancel = Button(winadd,text="Cancel",font=("Helvetica", 8),command=winadd.destroy)
    cancel.place(x=5,y=85 if intro_part else 105,anchor="sw")
    save = Button(winadd,text="OK",font=("Helvetica", 8),command=save_cfg)
    save.place(x=275,y=85 if intro_part else 105,anchor="se")

    try:
        while intro.wm_state() == "normal":
            winadd.update()
    except TclError:
        return

def remove():
    if intro_part: del cfg["servers"][server]["logins"][users.selection_get()]
    else: del cfg["servers"][servers.selection_get()]
    cf = open("meower95.conf","w")
    json.dump(cfg,cf)
    cf.close()
    log("Removed",servers.selection_get(),"from the", "user" if intro_part else "server", "list.")
    refresh_intro()

cf = open("meower95.conf","r")
cfg = json.load(cf)
cf.close()

intro = Tk()
intro.geometry("450x210")
intro.title("Meower95 - Quick login")

logo = PhotoImage(file=os.path.realpath('meower16.png'))
intro.wm_iconphoto(False, logo)

welcome = Label(intro, font=("Helvetica", 10))
servers = Listbox(intro, font=("Helvetica", 10))
user_title = Label(intro, text="Select your user account:", font=("Helvetica", 8))
users = Listbox(intro, font=("Helvetica", 8))
bback = Button(intro, text="< Back",command=back,font=("Helvetica", 8),state=DISABLED)
bnext = Button(intro,command=next,font=("Helvetica", 8))
badd = Button(intro, text="Add...",command=add,font=("Helvetica", 8))
bdel = Button(intro, text="Remove",command=remove,font=("Helvetica", 8))
sep = ttk.Separator(intro,orient='horizontal')

introsplash = PhotoImage(file=os.path.realpath('intro.png'))

bback.place(x=130,y=205,anchor="sw")
bnext.place(x=440,y=205,anchor="se")
badd.place(x=280,y=205,anchor="se")
bdel.place(x=280,y=205,anchor="sw")
sep.place(x=135,y=172,width=300,anchor="w")
introcanvas = Canvas(width=120,
                        height=196,
                        relief="flat")
introcanvas.create_image(0, 0, image=introsplash, anchor="nw")
introcanvas.place(x=3,y=5)

refresh_intro()

try:
    while intro.wm_state() == "normal" and intro_part < 2:
        intro.update()
        try: welcome.configure(text=welcome_messages[welcome_count])
        except IndexError: exit()
    intro.quit()
    intro.destroy()
except TclError:
    pass

if not server or not user: exit()

cfg["lastsession"] = {}
cfg["lastsession"]["server"] = server
cfg["lastsession"]["user"] = user
cf = open("meower95.conf","w")
json.dump(cfg,cf)
cf.close()

def backend():
    call(["python3", "backend.py"])

def donothing():print("boo")

window = Tk()
window.geometry("600x360")
window.resizable(0,0)
window.title("Meower95")

logo = PhotoImage(file=os.path.realpath('meower16.png'))
window.wm_iconphoto(False, logo)

proc = multiprocessing.Process(target=backend, args=())
proc.start()

def sendhttp(link,content):
    log("Sending", content, "to", cfg["servers"][server]["http"] + link, safe = True)
    req = urllib.request.Request(cfg["servers"][server]["http"] + link, headers={'User-Agent': 'Meower95'})
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Username', user)
    req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    jsondata = json.dumps({"content": content,"username":user,"pswd":cfg["servers"][server]["logins"][user]}).encode('utf-8')
    req.add_header('Content-Length', len(jsondata))
    return urllib.request.urlopen(req, jsondata)

def readhttp(link):
    log("Reading", cfg["servers"][server]["http"] + link, safe = True)
    req = urllib.request.Request(cfg["servers"][server]["http"] + link, headers={'User-Agent': 'Meower95'})
    url = urllib.request.urlopen(req)
    data = json.load(url)
    
    return data

def send_msg(event):
    sendhttp("home",entry.get())
    entry.delete(0,END)
    
def get_users(user):
    url = urllib.request.urlopen(cfg["servers"][server]["http"] + "users/" + user)
    data = json.load(url)

    return data

def insert_home():
    text = ""
    home = readhttp("home?autoget=1")["autoget"]
    home.reverse()
    
    messages.tag_remove(0.0,END)
    messages.configure(state=NORMAL)
    messages.delete(0.0,END)
    for i in range(0,len(home)):
        home[i]["u"] = home[i]["u"].replace("\n","")
        messages.mark_set(str(i),END)
        
        messages.insert(END,str(home[i]["u"]+': '+home[i]["p"]+"\n").encode('utf-16', 'surrogatepass').decode('utf-16'))

        messages.tag_add(str(i),str(int(messages.index(str(i)).split(".")[0])-2)+".0", str(int(messages.index(str(i)).split(".")[0])-2)+"."+str(len(home[i]["u"])))
        messages.tag_config(str(i),foreground="#000080")
        
    messages.configure(state=DISABLED)

print("setting up widgets...",end="")

menubar = Menu(window,relief=FLAT, font=('Helvetica', 8))
filemenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
filemenu.add_command(label="New", command=donothing, font=('Helvetica', 8))
filemenu.add_command(label="Open", command=donothing, font=('Helvetica', 8))
filemenu.add_command(label="Save", command=donothing, font=('Helvetica', 8))
filemenu.add_command(label="Save as...", command=donothing, font=('Helvetica', 8))
filemenu.add_command(label="Close", command=donothing, font=('Helvetica', 8))

filemenu.add_separator()
filemenu.add_command(label="Exit", command=window.quit, font=('Helvetica', 8))
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing, font=('Helvetica', 8))
editmenu.add_separator()
editmenu.add_command(label="Cut", command=donothing, font=('Helvetica', 8))
editmenu.add_command(label="Copy", command=donothing, font=('Helvetica', 8))
editmenu.add_command(label="Paste", command=donothing, font=('Helvetica', 8))
editmenu.add_command(label="Delete", command=donothing, font=('Helvetica', 8))
editmenu.add_command(label="Select All", command=donothing, font=('Helvetica', 8))

menubar.add_cascade(label="Edit", menu=editmenu, font=('Helvetica', 8))
helpmenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
helpmenu.add_command(label="Help Index", command=donothing, font=('Helvetica', 8))
helpmenu.add_command(label="About...", command=donothing, font=('Helvetica', 8))
menubar.add_cascade(label="Help", menu=helpmenu, font=('Helvetica', 8))

messages = Text(state=DISABLED, font=('Courier', 12),wrap=WORD)
messages.place(x=128,y=0,height=320,width=472)

channels = Listbox(font=('Helvetica', 8))
channels.place(x=0,y=0,width=128,height=360)

userlabel = Label(text=user+":", font=('Helvetica', 8))
userlabel.place(x=130,y=340,anchor="w")

entry = Entry(relief="ridge", font=('Courier', 12))
entry.place(x=390,y=340,width=360,anchor="center")

entry.bind("<Return>",send_msg)

window.config(menu=menubar)

ws_data = {}
print("done!")

print("inserting messages... ",end='')
insert_home()

print("done!")

try:
    while True:
        try:
            if not window.winfo_exists():
                break
        except:
            break
        try:
            transfer = open("TRANSFER","r")
            result = transfer.read()
            if result != '':
                transfer.close()
                print("new transfer data:",result)
                result = json.loads(result)
                try:
                    if result["cmd"] == "direct":
                        if result["val"]["mode"] == "auth":
                            ws_data["userdata"] = result["val"]
                            log("Auth data received.")
                        elif result["val"]["mode"] == 1:
                            insert_home()
                            log("New message, updating message list.")
                        else:
                            log(f'Unknown direct websocket data "{["val"]["mode"]}". still running doe ;3')
                    else:
                        ws_data[result["cmd"]] = result["val"]
                except KeyError:
                    ws_data[result["cmd"]] = result["val"]
                transfer = open("TRANSFER","w")
                transfer.write("")
            transfer.close()
        except FileNotFoundError:
            pass
        window.update()
except Exception as Error:
    os.system("kill -15 " + str(proc.pid + 2))
    raise Error
os.system("kill -15 " + str(proc.pid + 2))
print("see ya")