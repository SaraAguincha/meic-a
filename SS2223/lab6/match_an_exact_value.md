# Challenge `Match an Exact Value` writeup

- Vulnerability:
  - _Endpoint has a **buffer overflow** vulnerability_
- Where:
  - _`buffer` endpoint_
- Impact:
  - _Allows to **print the Congratulations message** without having the authority to by making a buffer overflow in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22152`. After the session is established we will can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 32 bytes, and the input is being read using the `gets` function. This means that the input can be bigger than the buffer, and we can make it overflow. This is what we call a **buffer overflow** vulnerability.

Similar to the previous exercise, we will first calculate the size of the buffer and then fill it with `A` characters. This will make the buffer fully filled with `A` characters, so then we can add the value that its being compared to so that it enters the if clause. The request we used and its corresponding payload was:

```python
msg = (b"A"*0x40 + b"dcba")
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()
```

The string dcba is in hexadecimal, so it is 0x61626364. Its also important to take into account that the representation of the string is in little endian, so the value is actually 0x64636261, and this is the value that is being compared to!

Now, we can see that the server returned the message `Congratulations, you win!!! You correctly got the variable to the right value`. This means that we have successfully exploited the vulnerability and obtained the `flag`.

## Script

The script used can be found [here](match_an_exact_value_poc.py)