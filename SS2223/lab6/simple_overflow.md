# Challenge `Simple Overflow` writeup

- Vulnerability:
  - _Endpoint has a **buffer overflow** vulnerability_
- Where:
  - _`buffer` endpoint_
- Impact:
  - _Allows to **print the message YOU WIN!** without having the authority to by making a buffer overflow in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22151`. After the session is established we will can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 64 bytes, and the input is being read using the `gets` function. This means that the input can be bigger than the buffer, and we can make it overflow. This is what we call a **buffer overflow** vulnerability.

Since we now know where the vulnerability is, we can start making a payload to exploit it. We will use the following payload:

```python
print("A"*0x60)
```

Even though it did work, we opted to make it a bit more dignified. For that, instead of using a random big string, we will first calculate the size of the buffer and then fill it with `A` characters. This will make the buffer fully filled with `A` characters, so then we can add just one more character to make it overflow. The request we used and its corresponding payload was:

```python
msg = (b"A"*0x81)
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()
```

Now, we can see that the server returned the message `YOU WIN!`. This means that we have successfully exploited the vulnerability and obtained the `flag`.


## Script

The script used can be found [here](simple_overflow_poc.py)
