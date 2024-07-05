import urllib.request, json, os, time, random, base64
from tkinter import *
from tkinter import ttk
from os.path import exists
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
    lf.write(logput + "\n")
    lf.close()
    if safe:
        lf = open("meower95.safelog","a" if exists("meower95.safelog") else "w")
        lf.write(logput + "\n")
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
useragent = ""
for i in range(0,8):
    useragent += random.choice("qwertyuiopasdfghjklzxcvbnm1234567890")

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
            return
    else:
        try:
            if servers.selection_get() in cfg["servers"].keys():
                server = servers.selection_get()
            else:
                return
        except TclError:
            welcome_count += 1
            try: welcome.configure(text=welcome_messages[welcome_count])
            except IndexError: intro.destroy()
            return
    
    intro_part += 1
    refresh_intro()

def register(username,password):
    req = urllib.request.Request(cfg["servers"][server]["http"] + "auth/register", headers={'User-Agent': useragent})
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps({"username":username,"password":password}).encode('utf-8')
    req.add_header('Content-Length', len(jsondata))
    return urllib.request.urlopen(req, jsondata)

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
            if cfg["servers"][entry1.get()]["http"][len(cfg["servers"][entry1.get()]["http"])] != "/":
                cfg["servers"][entry1.get()]["http"] += "/"
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
        reg = Button(winadd,text="Register account",font=("Helvetica", 8),state=DISABLED,command=lambda: register(entry1.get(),entry2.get()) )
        reg.place(x=140,y=85,anchor="s")
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
user_title = Label(intro, text="Select your user account:", font=("Helvetica", 10))
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
if not "settings" in cfg:
    cfg["settings"] = {"emoji":True,"markdown":True,"avatars":True,"msgdel":False,"discordcorrupt":False,"base64":False}
cfg["lastsession"] = {}
cfg["lastsession"]["server"] = server
cfg["lastsession"]["user"] = user
refresh_conf()

window = Tk()
window.resizable(0,0)
window.title("Meower95")

logo = PhotoImage(file=os.path.realpath('assets/meower16.png'))
window.wm_iconphoto(False, logo)

proc = sp.Popen([executable,'backend.py'])
status = sp.Popen.poll(proc)

def sendhttp(link,content):
    log("Sending", content, "to", cfg["servers"][server]["http"] + link, safe = True)
    req = urllib.request.Request(cfg["servers"][server]["http"] + link, headers={'User-Agent': useragent})
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Username', user)
    req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    jsondata = json.dumps({"content": content,"username":user,"pswd":cfg["servers"][server]["logins"][user]}).encode('utf-8')
    req.add_header('Content-Length', len(jsondata))
    return urllib.request.urlopen(req, jsondata)

def readhttp(link):
    log("Reading", cfg["servers"][server]["http"] + link, safe = True)
    req = urllib.request.Request(cfg["servers"][server]["http"] + link, headers={'User-Agent': useragent})
    req.add_header('Username', user)
    try:
        req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    except KeyError:
        pass
    try:
        url = urllib.request.urlopen(req)
        data = json.load(url)
        
        return data
    except urllib.error.URLError as e:
        return {}

def edit_msg(id="",content=""):
    req = urllib.request.Request(cfg["servers"][server]["http"] + "posts?id=" + id, headers={'User-Agent': useragent}, method='PATCH')
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    req.add_header('Username', user)
    req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    jsondata = json.dumps({"content": content,"username":user,"pswd":cfg["servers"][server]["logins"][user]}).encode('utf-8')
    req.add_header('Content-Length', len(jsondata))
    return urllib.request.urlopen(req, jsondata)

def del_msg(id=""):
    req = urllib.request.Request(cfg["servers"][server]["http"] + "posts?id=" + id, headers={'User-Agent': useragent}, method='DELETE')
    req.add_header('Username', user)
    req.add_header('Token', ws_data["userdata"]["payload"]["token"])
    return urllib.request.urlopen(req)

def send_msg(event):
    global last_message
    if entry.get() != "":
        text = entry.get()
        if cfg["settings"]["base64"]:
            text = "ec[Meower95]:"+str(base64.b64encode(bytes(text,"utf8")),"utf8")
        entry.delete(0,END)
        if cfg["settings"]["discordcorrupt"]:
            text_json = json.load(sendhttp(channel,"From "+user+" to everyone except users of the Discord Bridge."))["_id"]
            edit_msg(text_id,text_json["_id"])
        else:
            text_json = json.load(sendhttp(channel,text))
        last_message = text_json
    
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

def settings():
    global ivars
    def setvar(variable,widget):
        cfg["settings"][variable] = widget.instate(['selected'])
        refresh_conf()
    settings = Tk()
    settings.title("Meower95 - Settings")
    settings.geometry("480x320")
    settings.resizable(0,0)
    
    sstyle = ttk.Style(settings)
    sstyle.configure("TNotebook",font=("Helvetica",10))
    
    notebook = ttk.Notebook(settings)
    notebook.place(x=5,y=5,width=470,height=312)

    misc = Frame(notebook)
    sounds = Frame(notebook)
    hacks = Frame(notebook)

    notebook.add(misc,text="Misc.")
    #notebook.add(sounds,text="Sound") cant test it on my netbook :(
    notebook.add(hacks,text="Hacks")
    # Misc
    emoji = ttk.Checkbutton(misc,text="Convert text emojis into pictures")
    emoji.configure(command=lambda: setvar("emoji",emoji))
    emoji.place(x=30,y=20)
    markdown = ttk.Checkbutton(misc,text="Markdown support",state=DISABLED)
    markdown.configure(command=lambda: setvar("markdown",markdown))
    markdown.place(x=30,y=50)
    avatars = ttk.Checkbutton(misc,text="Load avatars")
    avatars.configure(command=lambda: setvar("avatars",avatars))
    avatars.place(x=30,y=80)
    
    msgdel = ttk.Checkbutton(hacks,text="Don't hide messages on deletion")
    msgdel.configure(command=lambda: setvar("msgdel",msgdel))
    msgdel.place(x=30,y=20)
    discordcorrupt = ttk.Checkbutton(hacks,text="Corrupt messages for Discord Bridge")
    discordcorrupt.configure(command=lambda: setvar("discordcorrupt",discordcorrupt))
    discordcorrupt.place(x=30,y=50)
    base64 = ttk.Checkbutton(hacks,text="Base64 encryption")
    base64.configure(command=lambda: setvar("base64",base64))
    base64.place(x=30,y=80)
    
    for i in cfg["settings"].keys():
        eval(i).state(['!alternate'])
        if cfg["settings"][i]: eval(i).state(['selected'])
    
    while True:
        settings.update()
        try:
            if not settings.winfo_exists(): break
        except TclError:
            break
def edit_gui(post):
    if type(post) == dict:
        def finish_editing():
            text = edittext.get(0.0,END).removesuffix("\n")
            if cfg["settings"]["base64"]:
                text = "ec[Meower95]:"+str(base64.b64encode(bytes(text,"utf8")),"utf8")
            edit_msg(post["_id"],text)
            winedit.destroy()
        
        winedit = Tk()
        winedit.geometry("480x240")
        winedit.resizable(0,0)
        
        edittext = Text(winedit)
        edittext.place(x=5,y=5,width=470,height=190)
        Button(winedit,text="Cancel",command=winedit.destroy).place(x=5,y=235,anchor="sw")
        Button(winedit,text="Edit!",command=finish_editing).place(x=475,y=235,anchor="se")
        
        chan = channel_by_id(post["_id"])
        text = home[chan][index_by_id(post["_id"],chan)]["p"]
        
        try:
            if text[0:3] == "ec[":
                text = str(base64.b64decode(text.split("]:")[len(text.split("]:"))-1]),"utf8")
            if text[0:3] == "rr:":
                text = str(base64.b64decode(text[3:len(text)-1]),"utf8")
        except IndexError:
            pass
        except UnicodeError:
            pass
        except base64.binascii.Error:
            pass
        edittext.insert(0.0,text)
        
        while True:
            winedit.update()
            try:
                if not winedit.winfo_exists(): break
            except TclError:
                break

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

home = {}
last_message = None
imagecache = {}

def load_image(id,name):
    if not exists(os.path.realpath("assets/cache/" + name)):
        url = urllib.request.Request("https://uploads.meower.org/attachments/"+id+"/"+name, headers={'User-Agent': 'Meower95',"Username":user})
        url.add_header('Token', ws_data["userdata"]["payload"]["token"])

        img = urllib.request.urlopen(url)
        
        image = open(os.path.realpath("assets/cache/" + name),"wb")
        image.write(img.read())
        image.close()
    return os.path.realpath("assets/cache/" + name)

def insert_home():
    text = ""
    messages.tag_remove(0.0,END)
    messages.configure(state=NORMAL)
    messages.delete(0.0,END)
    if channel not in home:
        try:
            home[channel] = readhttp(channel + "?autoget=1")["autoget"]
        except KeyError as e:
            messages.insert(END,"Cannot connect to the server, try again later.\n\n",("nonet"))
            messages.tag_configure("nonet",foreground="gray")
            messages.image_create(END, image = emojis["X("])
            return
            
        home[channel].reverse()
    for i in range(0,len(home[channel])):
        try:
            if home[channel][i]["p"][0:3] == "ec[":
                home[channel][i]["p"] = str(base64.b64decode(home[channel][i]["p"].split("]:")[len(home[channel][i]["p"].split("]:"))-1]),"utf8")
            if home[channel][i]["p"][0:3] == "rr:":
                home[channel][i]["p"] = str(base64.b64decode(home[channel][i]["p"][3:len(home[channel][i]["p"])]),"utf8")
        except IndexError:
            pass
        except UnicodeError:
            pass
        except base64.binascii.Error:
            pass
        home[channel][i]["u"] = home[channel][i]["u"].replace("\n","")
        messages.mark_set(str(i),END)
        if home[channel][i]["u"] in ["Discord"]: #known bridges, maybe add phone support later (if it even works today)
            color = "#800080"
            username = home[channel][i]["p"].split(": ")[0]
            text = ": ".join(home[channel][i]["p"].split(": ")[1:len(home[channel][i]["p"].split(":"))]).encode('utf-16', 'surrogatepass').decode('utf-16')
        else:
            color = "#000080"
            username = home[channel][i]["u"]
            text = home[channel][i]["p"].encode('utf-16', 'surrogatepass').decode('utf-16')
        messages.insert(END,username,"u_"+str(i))
        if home[channel][i]["isDeleted"]:
            messages.insert(END," (deleted)",("p_"+home[channel][i]["_id"],"smallfont"))
        elif "edited_at" in home[channel][i]:
            messages.insert(END," (edited)",("p_"+home[channel][i]["_id"],"smallfont"))
        messages.insert(END,": ",("p_"+home[channel][i]["_id"]))
        messages.tag_configure("u_"+str(i),foreground=color,font=("Helvetica",12))
        messages.tag_bind("u_"+str(i),"<Button-1>", lambda event, u=user: 
                            view_user(u))
        text = process_text(text.removesuffix("@"))
        for t in text:
            if t in emojis.keys():
                messages.image_create(END, image = emojis[t])
            else:
                messages.insert(END,t,("p_"+home[channel][i]["_id"]))
        if username == user:
            messages.tag_bind("p_"+home[channel][i]["_id"],"<Button-1>",
                              lambda event, t=home[channel][i]: edit_gui(t))
            messages.tag_bind("p_"+home[channel][i]["_id"],"<Button-3>",
                              lambda event, t=home[channel][i]["_id"]: del_msg(t))
        else:
            messages.tag_bind("p_"+home[channel][i]["_id"],"<Button-1>",
                              lambda event, t=f'@{home[channel][i]["u"]} [{home[channel][i]["_id"]}]': entry.insert(0,t))
        if home[channel][i]["isDeleted"]:
            messages.tag_configure("p_"+home[channel][i]["_id"],foreground="gray")
        for a in home[channel][i]["attachments"]:
            if a["mime"] in ("image/png","image/pgm","image/ppm","image/gif") and a["size"] < 2500000:
                try:
                    if not a["id"] in imagecache.keys():
                        imagecache[a["id"]] = PhotoImage(file=os.path.realpath("assets/cache/") + a["filename"] if exists(os.path.realpath("assets/cache/") + a["filename"]) else load_image(a["id"],a["filename"]))
                        if imagecache[a["id"]].width() > 480:
                            imagecache[a["id"]] = imagecache[a["id"]].subsample(int(a["width"]/480)+1)
                    messages.insert(END,"\n")
                    messages.image_create(END, name=a["id"], image=imagecache[a["id"]])
                    messages.insert(END,"\n")
                except KeyError:
                    pass
                except TclError:
                    pass
            
        messages.insert(END,"\n")
    
    messages.yview(END)
    messages.tag_configure("smallfont",font=("Helvetica",10))
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
            if cfg["settings"]["avatars"]:
                if u in pfps:
                    userlist.insert("",END,text=" "+u,image=pfps[u])
                else:
                    if not u in usrcache:
                        usrcache[u] = readhttp(f"users/{u}")
                    if str(usrcache[u]['pfp_data']) in pfps:
                        userlist.insert("",END,text=" "+u,image=pfps[str(usrcache[u]['pfp_data'])])
                    else:
                        userlist.insert("",END,text=" "+u)
            else:
                userlist.insert("",END,text=" "+u)
            window.update()
        

def refresh_view():
    global cfg
    for i in (channels,messages,userlist):
        i.place_forget()
    if not "view" in cfg:
        cfg["view"] = 7
        refresh_conf()
    show = bin(cfg["view"]).removeprefix("0b")
    show = "0" * (3 - len(show)) + show
    show = [show]
    for i in show[0]:
        show.append(bool(int(i)))
    del show[0]
    window.geometry(str(472 + (show[0] + show[2]) * 128) + ("x360" if show[1] else "x320"))
    messages.place(x=128 if show[0] else 0,y=0,height=320,width=460)
    scrollbar.place(x=588 if show[0] else 460,y=0,height=360 if show[1] else 320,width=12)
    if show[0]: channels.place(x=0,y=0,width=128,height=360 if show[1] else 320)
    if show[1]: entry.place(x=148 if show[0] else 20,y=340,width=420,anchor="w")
    if show[2]: userlist.place(x=600 if show[0] else 472,y=0,width=128,height=360)

def toggle_view(index):
    show = bin(cfg["view"]).removeprefix("0b")
    show = "0" * (3 - len(show)) + show
    show = [show]
    for i in show[0]:
        show.append(bool(int(i)))
    del show[0]
    show[index] = not show[index]
    for i in range(0,len(show)):
        show[i] = str(int(show[i]))
    cfg["view"] = int("".join(show),2)
    refresh_conf()
    refresh_view()    

channel = "home"
channellist={}
def change_channel(event):
    global channel
    if channels.selection_get() != "Home":
        channel_id = channellist[channels.selection_get()]
        channel = "posts/" + channel_id
    else:
        channel = "home"
    insert_home()
    
def index_by_id(id,chan):
    for m in range(0,len(home[chan])):
        if home[chan][m]["_id"] == id:
            return m
    raise ValueError("id not found")
def channel_by_id(id):
    for c in home.keys():
        for m in home[c]:
            if m["_id"] == id:
                return c
    raise ValueError("id not found")

def view_user(name):
    try:
        if type(name) == str:
            accountinfo = readhttp("users/"+name)
        elif type(name.widget) == ttk.Treeview:
            accountinfo = readhttp("users/"+userlist.item(userlist.focus())["text"].removeprefix(" "))

        lastseen = time.gmtime(accountinfo["last_seen"])

        userwin = Toplevel()
        userwin.title("Meower95 - "+accountinfo["_id"])
        userwin.geometry("240x180")
        if exists(f'assets/pfps/{accountinfo["pfp_data"]}.png') or exists(f'assets/pfps/{accountinfo["_id"]}.png'):
            avatar = PhotoImage(file=os.path.realpath(f'assets/pfps/{accountinfo["_id"]}.png' if exists(f'assets/pfps/{accountinfo["_id"]}.png') else f'assets/pfps/{accountinfo["pfp_data"]}.png'))
            Label(userwin,image=avatar).place(x=8,y=8)

        userlabel = Label(userwin,text=accountinfo["_id"],font=("Helvetica",14))
        userlabel.place(x=28,y=16,anchor="w")

        quote = Label(userwin,text=accountinfo["quote"],wraplength=100,justify=LEFT,font=("Helvetica",8))
        quote.place(x=8,y=32,width=100,height=120)

        ttk.Separator(userwin,orient="vertical").place(x=120,y=32,height=120,anchor="n")

        chatswith = Listbox(userwin,font=("Helvetica",10))
        chatswith.place(x=128,y=32,width=105,height=120)
        
        onlinep = PhotoImage(file = os.path.realpath("assets/online.png" if accountinfo["_id"] in ws_data["ulist"].split(";") else "assets/offline.png"))
        onlinei = Label(userwin,image=onlinep).place(x=8,y=164)

        offline_text = "Last seen on " + str(lastseen[2]) + (('st','nd')[lastseen[2]-1] if lastseen[2] < 2 else 'th') + " of " + ('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December')[lastseen[1]-1] + " " + str(lastseen[0]) + " " + str(lastseen[3]) + ":" + str(lastseen[4])
        online = Label(userwin,text="Online" if accountinfo["_id"] in ws_data["ulist"].split(";") else offline_text,font=("Helvetica",8))
        online.place(x=20,y=160)
        
        for chat in readhttp("chats")["autoget"]:
            if not chat["type"] and accountinfo["_id"] in chat["members"]:
                chatswith.insert(END,chat["nickname"])

        while True:
            userwin.update()
            try:
                if not userwin.winfo_exists(): break
            except TclError:
                break
    except urllib.error.HTTPError:
        pass

log("setting up widgets...",safe=True)

style = ttk.Style()
style.configure('.', font=('Helvetica', 8))

menubar = Menu(window,relief=FLAT, font=('Helvetica', 8))
mainmenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
mainmenu.add_command(label="Settings", command=settings, font=('Helvetica', 8))
mainmenu.add_separator()
mainmenu.add_command(label="Exit", command=window.destroy, font=('Helvetica', 8))
menubar.add_cascade(label="Meower95", menu=mainmenu)

viewmenu = Menu(menubar, tearoff=0, font=('Helvetica', 8))
viewmenu.add_command(label="Chat sidebar", command=lambda: toggle_view(0), font=('Helvetica', 8))
viewmenu.add_command(label="Chat entry", command=lambda: toggle_view(1), font=('Helvetica', 8))
viewmenu.add_command(label="User sidebar", command=lambda: toggle_view(2), font=('Helvetica', 8))
menubar.add_cascade(label="View", menu=viewmenu)

messages = Text(state=DISABLED, font=('Courier', 12),wrap=WORD)
scrollbar = ttk.Scrollbar(command=messages.yview)
messages.config(yscrollcommand = scrollbar.set)
channels = Listbox(font=('Helvetica', 8))
channels.insert(END,"Home")
userlist = ttk.Treeview(padding=0,show='tree',selectmode='browse')
userlist.bind("<<TreeviewSelect>>",view_user)
entry = Entry(relief="ridge",font=('Courier', 12))
entry.insert(0,"Waiting for authentification...")
entry.configure(state=DISABLED)
entry.bind("<Return>",send_msg)
entry.bind("<Up>",lambda event: edit_gui(last_message))
refresh_view()
window.config(menu=menubar)

ws_data = {}
insert_home()

try:
    while True:
        try:
            if not window.winfo_exists():
                break
        except:
            break
        try:
            transfer = open("TRANSFER","r")
            deleted = 0
            try:
                result = json.load(transfer)
            except json.decoder.JSONDecodeError:
                transfer = open("TRANSFER","w")
                transfer.close()
                result = ''
            if result != '':
                transfer.close()
                transfer = open("TRANSFER","w")
                transfer.write("")
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
                            if ws_data["userdata"]["payload"]["account"]["ban"]["state"] == "perm_restriction" and ws_data["userdata"]["payload"]["account"]["ban"]["restrictions"] == 31:
                                entry.insert(0,f'You\'re banned for {ws_data["userdata"]["payload"]["account"]["ban"]["reason"]} :(')
                                entry.configure(state=DISABLED)
                            else:
                                entry.configure(state=NORMAL)
                            chats = readhttp("chats")["autoget"]
                            for i in chats:
                                channels.insert(END, i["members"][0] if i["type"] else i["nickname"])
                                channellist[i["members"][0] if i["type"] else i["nickname"]] = i["_id"]
                            channels.bind("<<ListboxSelect>>",change_channel)
                            insert_home()
                        elif result["val"]["mode"] == 1:
                            if result["val"]["post_origin"] == "home":
                                home["home"].append(result["val"])
                            else:
                                home["posts/"+result["val"]["post_origin"]].append(result["val"])
                            insert_home()
                        elif result["val"]["mode"] == "update_post":
                            chan = channel_by_id(result["val"]["payload"]["_id"])
                            home[chan][index_by_id(result["val"]["payload"]["_id"],chan)] = result["val"]["payload"]
                            home[chan][index_by_id(result["val"]["payload"]["_id"],chan)]["edited"] = True
                            insert_home()
                        elif result["val"]["mode"] == "delete":
                            chan = channel_by_id(result["val"]["id"])
                            if cfg["settings"]["msgdel"]:
                                home[chan][index_by_id(result["val"]["id"],chan)]["isDeleted"] = True
                            else:
                                try:
                                    del home[chan][index_by_id(result["val"]["id"],chan)]
                                except ValueError:
                                    pass
                            insert_home()
                        elif result["val"]["mode"] == "banned":
                            entry.delete(0,END)
                            entry.configure(state=NORMAL)
                            if result["val"]["payload"]["state"] == "temp_ban" and result["val"]["payload"]["expires"] > time.time() or result["val"]["payload"]["state"] == "perm_ban":
                                entry.insert(END,f'You\'re banned for {result["val"]["payload"]["reason"]} :(')
                                entry.configure(state=DISABLED)
                        log('Unrecognized direct websocket data.',safe=True)
                else:
                    ws_data[result["cmd"]] = result["val"]
                    if result["cmd"] == "ulist":
                        refresh_users()
               
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