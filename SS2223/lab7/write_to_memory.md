# Challenge `Write to Memory` writeup

- Vulnerability:
  - _Endpoint has a **format string** vulnerability_
- Where:
  - _`printf` endpoint_
- Impact:
  - _Allows to **read and write the stack values and arbitrary registers** without having the authority to by using the (vulnerable) printf function in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22192`. After the session is established we can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 128, and afterwards, in the function `vuln`, is printed. We can see that the `printf` function is being used to print the buffer, and it has a format string vulnerability. 

This means that we can send `%08x.` characters to print the stack values. We need to see where in the stack our buffer is and update the targets value to something different. To check the **target address** we used the gdb debugger with the corresponding **binary** file. To get it, we made a breakpoint in **vuln** and used the following command:

```bash
gdb-peda$ p &target
$4 = (unsigned int *) 0x804a040 <target>
```

Since we now have the address of the target we now need to know where in the stack the buffer starts. To do this we used the following payload:

```python
msg = (b"AAAA" + b"%08x."*20)
```

We obained: 
```bash
AAAAffffdc7c.0000007f.ffffdcd8.f7ffda74.00000001.f7fd3490.41414141.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.
Oops, not quite!
```

Because we used the string `AAAA` as a reference, we can see that the buffer starts in the 7th place. Having this information, we can now try to overwrite the target value. To do this we used the following payload:

```python
msg = (b"\x40\xa0\x04\x08.%7$n")
r.sendline(msg)
print(f"Flag: {r.recvall()}")
r.close()
```

Now, we can see that the server returned the `flag`. This means that we have successfully exploited the vulnerability and achieved our objective.

## Script

The script used can be found [here](write_to_memory_poc.py)