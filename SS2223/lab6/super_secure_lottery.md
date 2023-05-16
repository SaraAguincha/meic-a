# Challenge `Super Securety Lottery` writeup

- Vulnerability:
  - _Endpoint has a **buffer overflow** vulnerability_
- Where:
  - _`read` endpoint_
- Impact:
  - _Allows to **print the message YOU WIN!** without having the authority to by making a buffer overflow in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22161`. After the session is established we will can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer (guess) being used to store the input of the user. The buffer has a size of 8 bytes, and the input is being read using the `read` function, allowing to input up to 64 bytes. This means that the input can be bigger than the buffer, and we can make it overflow. This is what we call a **buffer overflow** vulnerability.

Since we now know where the vulnerability is, we can start by making a payload bigger than they expect. We will use the following code and payload:

```python
msg = (b"A"*0x80)
r.sendline(msg)

print(f"Message server sent:\n{r.recvline().decode()}\n")

r.close()
```

The payload is just a string of 'A' characters, with a size of 80 bytes.

Now, eventhough it was just a simple overflow, we can see that the server returned the message `Congratulations! You won the lottery`. This means that we have successfully exploited the vulnerability and obtained the `flag`.


## Script

The script used can be found [here](super_sercure_lottery_poc.py)