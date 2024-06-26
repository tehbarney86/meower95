import urllib.request, json, os, time
from tkinter import *
from tkinter import ttk
from os.path import exists
from subprocess import call
from urllib.request import ssl
from urllib.error import URLError
import subprocess as sp
from sys import executable

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

def refresh_conf():
    global cfg,cf
    cf = open("meower95.conf","w")
    json.dump(cfg,cf)
    cf.close()

welcome_messages = ("Select a server by clicking it's title on the list below:",
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
welcome_count = -1
intro_part = 0
server = user = None

def refresh_intro():
    users.delete(0,END)
    servers.delete(0,END)
    for i in (welcome,servers,user_title,users):
        i.place_forget()
    welcome.place_forget()
    bback.configure(state=DISABLED if intro_part == 0 else NORMAL)
    bnext.configure(text="Chat!" if intro_part else "Next >")
    if intro_part > 1:
        intro.destroy()
    elif intro_part:
        if "logins" in cfg["servers"][server]:
            for i in list(cfg["servers"][server]["logins"].keys()):
                users.insert(END,i)
        else:
            cfg["servers"][server]["logins"] = {}
            refresh_conf()
        user_title.place(x=130,y=5)
        users.place(x=130,y=30,width=310,height=135)
    else:
        if "servers" in cfg:
            for i in list(cfg["servers"].keys()):
                servers.insert(END,i)
        else:
            cfg["servers"] = {}
            refresh_conf()
            
        welcome.place(x=130,y=5)
        servers.place(x=130,y=30,width=310,height=135)
    
def next():
    global welcome_count,server,user,intro_part
    if intro_part: #replace with case, no documentation offline yk
        try:
            if users.selection_get() in cfg["servers"][server]["logins"].keys():
                user = users.selection_get()
            else:
                return
        except TclError as e:
            print(e)
            return
    else:
        try:
            if servers.selection_get() in cfg["servers"].keys():
                server = servers.selection_get()
            else:
                return
        except TclError as e:
            print(e)
            welcome_count += 1
            try: welcome.configure(text=welcome_messages[welcome_count])
            except IndexError: intro.destroy()
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
        refresh_conf()
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
    refresh_intro()

def remove():
    if intro_part: del cfg["servers"][server]["logins"][users.selection_get()]
    else: del cfg["servers"][servers.selection_get()]
    cf = open("meower95.conf","w")
    json.dump(cfg,cf)
    cf.close()
    log("Removed",servers.selection_get(),"from the", "user" if intro_part else "server", "list.")
    refresh_intro()

empty_conf = True
if not exists("meower95.conf"):
    empty_conf = False
    cf = open("meower95.conf","w")
    cf.close()
cf = open("meower95.conf","r")
try:
    cfg = json.load(cf)
except json.decoder.JSONDecodeError as error:
    print(cf.read())
    if empty_conf:
        jsonwin = Tk()
        jsonwin.title("Meower95 - Error")
        jsonwin.geometry("400x110")
        jsonwin.resizable(0,0)
        warnicon = PhotoImage(file=os.path.realpath('assets/warning.png'))
        Label(jsonwin, image=warnicon).place(x=5,y=10)
        Label(text='''Your configuration file (meower95.conf) might be corrupted.
Your old JSON file is saved to meower95.conf.bak,
and your current configuration will be reset.
sorry :(''', justify="left", font=("Helvetica", 10)).place(x=50,y=10)
        Button(jsonwin,text="Continue",command=jsonwin.destroy,font=("Helvetica", 10)).place(x=395,y=105,anchor="se")
        jsonwin.mainloop()
        
        cfb = open("meower95.conf.bak","w")
        cfb.write(cf.read())
        
        cfb.close()
        
        cfg = {}
        refresh_conf()
    else: cfg = {}
cf.close()

intro = Tk()
intro.geometry("450x210")
intro.title("Meower95 - Quick login")
intro.resizable(0,0)

logo = PhotoImage(file=os.path.realpath('assets/meower16.png'))
intro.wm_iconphoto(False, logo)

welcome = Label(intro, text="Welcome to Meower95! Select your server:", font=("Helvetica", 10))
servers = Listbox(intro, font=("Helvetica", 8))
user_title = Label(intro, text="Select your user account:", font=("Helvetica", 8))
users = Listbox(intro, font=("Helvetica", 8))
bback = Button(intro, text="< Back",command=back,font=("Helvetica", 8),state=DISABLED)
bnext = Button(intro,command=next,font=("Helvetica", 8))
badd = Button(intro, text="Add...",command=add,font=("Helvetica", 8))
bdel = Button(intro, text="Remove",command=remove,font=("Helvetica", 8))
sep = ttk.Separator(intro,orient='horizontal')

introsplash = PhotoImage(file=os.path.realpath('assets/intro.png'))

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
    intro.mainloop()
except TclError:
    pass

if not server or not user: exit()

cfg["lastsession"] = {}
cfg["lastsession"]["server"] = server
cfg["lastsession"]["user"] = user
refresh_conf()

def donothing():print("boo")

window = Tk()
window.resizable(0,0)
window.title("Meower95")

logo = PhotoImage(file=os.path.realpath('assets/meower16.png'))
window.wm_iconphoto(False, logo)

proc = sp.Popen([executable,'backend.py'])
status = sp.Popen.poll(proc)

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
    req.add_header('Username', user)
    try:
        req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    except KeyError:
        pass
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

emojis = {}
ef = open("assets/emojis/emojis.conf")
emojiconf = json.load(ef)
ef.close()
for e in emojiconf.keys():
    emojis[e] = PhotoImage(file=os.path.realpath(f'assets/emojis/{emojiconf[e]}'))

def process_text(text):
    result = []
    words = []
    for word in emojis.keys():
        last = 0
        for i in range(0,text.count(word)):
            words.append([text.index(word,last), word])
            last = text.index(word,last) + 1
    try:
        result.append(text[0:words[0][0]])
    except IndexError:
        return [text]
    for i in range(0,len(words)):
        result.append(words[i][1])
        try:
            result.append(text[words[i][0]+len(words[i][1]):words[i+1][0]])
        except IndexError:
            pass
    result.append(text[words[i][0]+len(words[i][1]):len(text)])
    return result
    
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
        if home[i]["u"] == "Discord":
            messages.insert(END,home[i]["p"].split(": ")[0])
            text = ": ".join(home[i]["p"].split(": ")[1:len(home[i]["p"].split(":"))]).encode('utf-16', 'surrogatepass').decode('utf-16')
        else:
            messages.insert(END,home[i]["u"])
            text = home[i]["p"].encode('utf-16', 'surrogatepass').decode('utf-16')
        text = process_text(text)
        messages.insert(END,': ')
        for i in text:
            if i in emojis.keys():
                messages.image_create(END, image = emojis[i])
            else:
                messages.insert(END,i)
        messages.insert(END,"\n")
    
    messages.yview(END)
    messages.configure(state=DISABLED)
    
pfps = {}
for p in os.listdir("assets/pfps/"):
    pfps[os.path.splitext(p)[0]] = PhotoImage(file=os.path.realpath(f'assets/pfps/{p}'))
usrcache = {}

def refresh_users():
    global pfpcache
    for i in userlist.get_children():
        userlist.delete(i)
    for u in ws_data["ulist"].split(";"):
        if u != "":
            if not u in usrcache:
                print(u)
                usrcache[u] = readhttp(f"users/{u}")
            if u in pfps:
                userlist.insert("",END,text=" "+u,image=pfps[u])
            elif str(usrcache[u]['pfp_data']) in pfps:
                userlist.insert("",END,text=" "+u,image=pfps[str(usrcache[u]['pfp_data'])])
            else:
                userlist.insert("",END,text=" "+u)
            
            window.update()

def refresh_view():
    global cfg
    for i in (channels,messages,userlist):
        i.place_forget()
    if not "view" in cfg:
        cfg["view"] = 1
        #refresh_conf()
    show = bin(cfg["view"]).removeprefix("0b")
    show = "0" * (2 - len(show)) + show
    show = [bool(int(show[0])),bool(int(show[1]))]
    window.geometry(str(472 + sum(show) * 128) + "x360")
    if show[0]: channels.place(x=0,y=0,width=128,height=360)
    messages.place(x=128 if show[0] else 0,y=0,height=320,width=472)
    if show[1]: userlist.place(x=600 if show[0] else 472,y=0,width=128,height=360)
    userlabel.place(x=130 if show[0] else 2,y=340,anchor="w")
    entry.place(x=390  if show[0] else 262,y=340,width=360,anchor="center")

def toggle_view(index):
    show = bin(cfg["view"]).removeprefix("0b")
    show = "0" * (2 - len(show)) + show
    show = [bool(int(show[0])),bool(int(show[1]))]
    show[index] = not show[index]
    cfg["view"] = int(f"{int(show[0])}{int(show[1])}",2)
    refresh_conf()
    refresh_view()    
    
print("setting up widgets...",end="")

style = ttk.Style()
style.configure('.', font=('Helvetica', 8))

menubar = Menu(window,relief=FLAT, font=('Helvetica', 8))
mainmenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
mainmenu.add_command(label="Switch server...", command=donothing, font=('Helvetica', 8))
mainmenu.add_command(label="Switch account...", command=donothing, font=('Helvetica', 8))
mainmenu.add_separator()
mainmenu.add_command(label="Exit", command=window.destroy, font=('Helvetica', 8))
menubar.add_cascade(label="Meower95", menu=mainmenu)

viewmenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
viewmenu.add_command(label="Chat sidebar", command=lambda: toggle_view(0), font=('Helvetica', 8))
viewmenu.add_command(label="User sidebar", command=lambda: toggle_view(1), font=('Helvetica', 8))
menubar.add_cascade(label="View", menu=viewmenu)

messages = Text(state=DISABLED, font=('Courier', 12),wrap=WORD)
channels = Listbox(font=('Helvetica', 8))
userlist = ttk.Treeview(padding=0,show='tree')
userlabel = Label(text=user+":", font=('Helvetica', 8))
entry = Entry(relief="ridge",font=('Courier', 12))
entry.insert(0,"Waiting for authentification...")
entry.configure(state=DISABLED)
entry.bind("<Return>",send_msg)
refresh_view()

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
            try:
                result = json.load(transfer)
            except json.decoder.JSONDecodeError:
                transfer = open("TRANSFER","w")
                transfer.close()
                result = ''
            if result != '':
                transfer.close()
                print("new transfer data:",result)
                if result ["cmd"] == "statuscode":
                    if type(result["val"]) == str:
                        if result["val"] == "E:020 | Kicked":
                            entry.configure(state=NORMAL)
                            entry.delete(0,END)
                            entry.insert(END,"You were kicked from this server :(")
                            entry.configure(state=DISABLED)
                        elif result["val"] == "E:018 | Account Banned":
                            entry.configure(state=NORMAL)
                            entry.delete(0,END)
                            entry.insert(END,"You were banned from this server :(")
                            entry.configure(state=DISABLED)
                elif result["cmd"] == "direct":
                    if "mode" in result["val"]:
                        if result["val"]["mode"] == "auth":
                            ws_data["userdata"] = result["val"]
                            log("Auth data received.",safe=True)
                            entry.configure(state=NORMAL)
                            entry.delete(0,END)
                            if ws_data["userdata"]["payload"]["account"]["ban"]["state"] == "perm_restriction":
                                entry.insert(0,f'You\'re banned for {ws_data["userdata"]["payload"]["account"]["ban"]["reason"]} :(')
                                entry.configure(state=DISABLED)
                            else:
                                entry.configure(state=NORMAL)
                        elif result["val"]["mode"] in (1,"delete","edit"):
                            insert_home()
                            log("New message, updating message list.",safe=True)
                        elif result["val"]["mode"] == "banned":
                            print(time.time(),result["val"]["payload"]["expires"] > time.time())
                            entry.delete(0,END)
                            entry.configure(state=NORMAL)
                            if result["val"]["payload"]["state"] == "temp_ban" and result["val"]["payload"]["expires"] > time.time() or result["val"]["payload"]["state"] == "perm_ban":
                                entry.insert(END,f'You\'re banned for {result["val"]["payload"]["reason"]} :(')
                                entry.configure(state=DISABLED)
                        log(f'Unknown direct websocket data. still running doe ;3',safe=True)
                else:
                    ws_data[result["cmd"]] = result["val"]
                    if result["cmd"] == "ulist":
                        refresh_users()
               
            transfer = open("TRANSFER","w")
            transfer.write("")
            transfer.close()
        except FileNotFoundError:
            pass
        window.update()
except Exception as Error:
    sp.Popen.terminate(proc)
    status = sp.Popen.poll(proc)
    raise Error
sp.Popen.terminate(proc)
status = sp.Popen.poll(proc)
print("see ya")