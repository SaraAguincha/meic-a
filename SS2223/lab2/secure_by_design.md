# Challenge `Secure by design` writeup

- Vulnerability:
  - _Endpoint is vulnerable to **Cookie poisoning**_
- Where:
  - _`Cookies`, more specific ['user']_
- Impact:
  - _Allows the user to have the **admin status**_

## Steps to reproduce
First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22056`. After the session is established 
the search to get the admin status begins.

Since there is not much information to start from gathering the html itself, we start by analyzing the cookies. A specific field named **user** seems to be our gateway to achieve the admin status. `Note`: This field is encoded in Base64.

```python
print(session.cookies.get_dict())
```

After several attempts with different inputs, even with special characters, the server would just read it as a normal string and ignore it since it was non-admin. However, there was an exception with one specific username. When the input given was **admin**, the server transformed it into **fake-admin**.
It would change the value of the field user from **admin, YWRtaW4=** to **fake-admin, ZmFrZS1hZG1pbg==**.

Seeing that the server changed this value, after looking again at the cookies, we set the cookie field `user` to `YWRtaW4=` 
which is **admin** in Base64, forcing the site to accept us as the **admin**, and request a **get**.

```python
session.cookies.set('user', 'YWRtaW4=', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')
r = session.get(SERVER) # refresh
```

Now, after reloading the page, we will have `admin status` and captured the flag.

## Script
The script used can be found [here](secure_by_design_poc.py).
