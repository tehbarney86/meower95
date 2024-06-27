from websockets.exceptions import ConnectionClosedError
from websockets.sync.client import connect
from os.path import exists
import json

def writefile():
    global websocket
    try:
        transfer = open("TRANSFER","w")
        recv = websocket.recv()
        print(recv)
        transfer.write(recv)
        transfer.close()
    except ConnectionClosedError:
        websocket = connect(cfg["servers"][server]["http"])
        websocket.send('{"cmd": "direct", "val": {"username": "' + user + '", "pswd": "' + cfg["servers"][server]["logins"][user] + '"}}')
        print("packet sent")

cf = open("meower95.conf","r")
cfg = json.load(cf)
cf.close()

websocket = connect(cfg["servers"][cfg["lastsession"]["server"]]["websocket"])
websocket.send('{"cmd": "direct", "val": {"cmd": "authpswd", "val": {"username": "' + cfg["lastsession"]["user"] + '", "pswd": "' + cfg["servers"][cfg["lastsession"]["server"]]["logins"][cfg["lastsession"]["user"]] + '"}}}')
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