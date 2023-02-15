import time
import json
import websocket
from requests import Session
from threading import Thread
URL_API = "https://api.betfiery.com"
WSS_BASE = "wss://api.betfiery.com"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

result_dict = None

session = Session()
session.request("GET", f"{URL_API}/socket.io/?EIO=4&transport=polling&t=OGFay0v", headers=HEADERS)
cookies = session.cookies.get_dict()


def get_ws_result():
    return result_dict


def on_message(ws, msg):
    global result_dict

    print("OLHA AÍ: ", msg)
    if msg == "3probe":
        print("SAPORRA É IGUAL")
        ws.send("5")


def on_error(ws, error):
    print(error)


def on_close(ws, status, msg):
    time.sleep(1)
    connect_websocket()


def on_pong(ws, msg):
    ws.send("3")


def on_open(ws):
    message = '2probe'
    ws.send(message)


def connect_websocket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"{WSS_BASE}/socket.io/?EIO=4&transport=websocket&sid={cookies['sid']}",
                                header=HEADERS,
                                on_open=on_open,
                                on_message=on_message,
                                on_close=on_close,
                                on_pong=on_pong,
                                cookie="; ".join(["%s=%s" % (i, j) for i, j in cookies.items()]),
                                )

    ws.run_forever(ping_interval=24,
                   ping_timeout=2,
                   ping_payload="3",
                   origin="https://betfiery.com",
                   host="api.betfiery.com")


Thread(target=connect_websocket, args=[]).start()
