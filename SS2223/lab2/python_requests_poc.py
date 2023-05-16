import requests
import re

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22053'

# Start session
session = requests.session()
r = session.get(SERVER)

def get_flag():
    while True:
        r = session.get(SERVER + "/more")
        numbers = re.findall(r'\d+',r.text) # regex filter only numbers
        if numbers[1] == numbers[2]:
            r = session.get(SERVER + "/finish")
            break
    print("The flag is: " + r.text)

get_flag()
