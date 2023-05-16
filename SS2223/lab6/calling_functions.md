# Challenge `Calling Functions` writeup

- Vulnerability:
  - _Endpoint has a **buffer overflow** vulnerability_
- Where:
  - _`buffer` endpoint_
- Impact:
  - _Allows to **print the Congratulations message** without having the authority to by making a buffer overflow in the server's code_

## Steps to reproduce

### TODO (review site link)
First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22153`. After the session is established we will can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 32 bytes, and the input is being read using the `gets` function. This means that the input can be bigger than the buffer, and we can make it overflow. This is what we call a **buffer overflow** vulnerability.

Similar to the previous exercise, we will first calculate the size of the buffer and then fill it with `A` characters. This will make the buffer fully filled with `A` characters, so then we can alter the value that the `fp` variable has with the **win function address**! By doing so, when the code reaches the if statement, it will see that the pointer has a value and will execute the function that is in that address. The request we used and its corresponding payload was:

```python
msg = (b"A"*0x20 + b"\xf1\x86\x04\x08")  
                                                       
r.sendline(msg)
print(f"Flag: {r.recvall().decode()}")

r.close()
```

Now, we can see that the server returned the message `Congratulations, you win!!! You successfully changed the code flow`. This means that we have successfully exploited the vulnerability and obtained the `flag`.


## Script

The script used can be found [here](calling_functions_poc.py)
