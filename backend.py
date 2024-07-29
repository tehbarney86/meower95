import websocket
from os.path import exists
import json

def writefile():
    global websocket
    try:
        recv = irun(lambda: websocket.recv())
        transfer = open("TRANSFER","w")
        transfer.write(recv)
        transfer.close()
    except Exception as e:
        print(e)
def irun(com):
    while True:
        try:
            return com()
        except Exception as e:
            if str(e) in ("[Errno -3] Temporary failure in name resolution","[Errno 101] Network is unreachable"):
                pass
            else:
                raise e
        

cf = open("meower95.conf","r")
cfg = json.load(cf)
cf.close()
websocket = websocket.WebSocket()
irun(lambda: websocket.connect(cfg["servers"][cfg["lastsession"]["server"]]["websocket"]))
irun(lambda: websocket.send('{"cmd": "direct", "val": {"cmd": "authpswd", "val": {"username": "' + cfg["lastsession"]["user"] + '", "pswd": "' + cfg["servers"][cfg["lastsession"]["server"]]["logins"][cfg["lastsession"]["user"]] + '"}}}'))
while True:
    try:
        while True:
            transfer = open("TRANSFER","r")
            if transfer.read() == "":
                break
            transfer.close()
        writefile()
    except FileNotFoundError:
        writefile()