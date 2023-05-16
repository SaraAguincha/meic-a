# Challenge `Python requests` writeup

- Vulnerability:
  - _Endpoint is vulnerable to **brute-force attacks**_
- Where:
  - _`/more` endpoint_
- Impact:
  - _Allows to find the server's **target** by enumeration_

## Steps to reproduce
First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22053`. After the session is established 
the search for the server's number begins. 

While in the loop, the brute-force requests start. Requests with `/more` are sent repeatedly, and after receiving the 
responses the numbers in them are extracted. 

Having the numbers, the **current** is compared to the **target**, and when equal, 
instead of making another `/more` request, it will be issued an `/finish`.

```python
while True:
    r = session.get(SERVER + "/more")
    numbers = re.findall(r'\d+',r.text) # regex filter only numbers
    if numbers[1] == numbers[2]:
        r = session.get(SERVER + "/finish")
        break
print("The flag is: " + r.text)
```
Now, we will have access to the server's `target number` giving us the flag.

## Script
The script used can be found [here](python_requests_poc.py)
