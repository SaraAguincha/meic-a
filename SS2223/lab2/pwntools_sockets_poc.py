from pwn import *

r = remote('mustard.stt.rnl.tecnico.ulisboa.pt', 22055)

# gets the initial numbers (target and current)
initial_numbers = re.findall(r'\d+',r.recvuntil(b"FINISH").decode()) # regex filter only numbers

target = initial_numbers[0]
r.sendline(b"MORE")

while True:
    numbers = re.findall(r'\d+',r.recvuntil(b"FINISH").decode())
    if numbers[1] == target:
        r.sendline(b"FINISH")
        flag = r.recvall().decode()
        break
    else:
        r.sendline(b"MORE")
print("The flag is: " + flag)
