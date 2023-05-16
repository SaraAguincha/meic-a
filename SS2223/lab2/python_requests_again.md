# Challenge `Python requests again` writeup

- Vulnerability:
  - _Endpoint is vulnerable to **brute-force attacks** and **Cookie poisoning**_
- Where:
  - _`/more` endpoint_
- Impact:
  - _Allows to find the server's **target** by enumeration and cookie poisoning_

## Steps to reproduce
First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22054`. After the session is established 
the search for the server's number begins. 

We can't start brute-forcing from the very beginning because there is something that keeps us from making more than one request to the server with the `/more`.
Since there is something being recorded (the tries), the cookies are analyzed and there is a field named **remaining_tries**.
```python
print(session.cookies.get_dict())
```

Since we now know the field that is stopping us, we can do multiple things. One possible option is to set the remaining 
tries to a relatively high number and then brute force it. Other option would be to just set the field tries every cycle of the while, 
but since it was not necessary and there would be **N cookie.set() commands** the first option was the one chosen.

```python
session.cookies.set('remaining_tries', '1000000', domain="mustard.stt.rnl.tecnico.ulisboa.pt", path='/')
```

While in the loop, the brute-force requests start. Requests with `/more` are sent repeatedly, and after receiving the 
responses the numbers in each one is extracted. Having the numbers, the **current** is compared to the **target**, and when equal, 
instead of making another `/more` request, it will be issued a `/finish`.

```python
while True:
        r = session.get(SERVER + "/more")
        numbers = re.findall(r'\d+',r.text)
        if numbers[1] == numbers[2]:
            r = session.get(SERVER + "/finish")
            break
        session.close()
        print(r.text)
    print("The flag is: " + r.text)
```

Now, we will have access to the server's `target number` giving us the flag.

## Script
The script used can be found [here](python_requests_again_poc.py)
