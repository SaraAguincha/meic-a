# Challenge `Pwntools sockets` writeup

- Vulnerability:
  - _Endpoint is vulnerable to **brute-force attacks**_
- Where:
  - _`/MORE` endpoint_
- Impact:
  - _Allows to find the server's **target** by enumeration_

## Steps to reproduce
First we need to connect to the server `http://mustard.stt.rnl.tecnico.ulisboa.pt` in the port `22055`. After the connection is established 
the search for the server's target begins.

The first thing before brute-forcing was to get the `target` number. To get it, we needed to receive the server's information until it 
asks us to choose what to insert. It was defined **'FINISH'** as a delimit, since it was the last word.
```python
r.recvuntil(b"FINISH").decode()
```
 After having the response we can just use a regex to filter the numbers in it.
 ```python
initial_numbers = re.findall(r'\d+',r.recvuntil(b"FINISH").decode())
target = initial_numbers[0]
```
Since the user always starts with **0**, before starting the brute-forcing a request with `MORE` is sent.
While in the loop, the cycle of receiving the information until the word **'FINISH'**, extracting the current and comparing to the
**target** is repeated.
```python
while True:
    numbers = re.findall(r'\d+',r.recvuntil(b"FINISH").decode())
    if numbers[1] == target:
        r.sendline(b"FINISH")
        flag = r.recvall().decode()
        break
    else:
        r.sendline(b"MORE")
```
Now, after some seconds, we will achieve the server's `target number` getting us the flag.

## Script
The script used can be found [here](pwntools_sockets_poc.py)
