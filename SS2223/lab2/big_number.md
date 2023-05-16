# Challenge `Big number` writeup

- Vulnerability:
  - _Endpoint is vulnerable to **brute-force attacks**_
- Where:
  - _`/number/guess` endpoint_
- Impact:
  - _Allows to find the server's **number** by enumeration_

## Steps to reproduce
First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22052`. After the session is established 
the search for the server's number begins. 

The algorithm used to make the search faster was **binary search** starting with making a guess right in 
the middle, **50000**. This choice was made because everytime a guess is made, the server will respond with either
**Higher or Lower**.

If the answer is `Higher` the **min** value will be updated with
the guess made. If its `Lower` the value updated will be the **max**. The following guess will be the number in the middle 
of the **max or min** depending on the response obtained.

``` python
guess = 50000
max = 100000
min = 1

while True:
    r = guess_number(guess)
    if r.text.find("Higher") != -1:
        min = guess
        guess = (max + guess)//2
    elif r.text.find("Lower") != -1:
        max = guess
        guess = (min + guess)//2
    else:
        break
```
When sending requests to the server with the new guess, the format used is `/number/<guess>`.
``` python
r = session.get(SERVER + "/number/" + str(guess))
```
Now, after some tries, the algorithm will converge to the target number and we will have access to the server's `number` giving us the flag!

## Script
The script used can be found [here](big_number_poc.py)
