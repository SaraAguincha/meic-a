# Challenge `Pickles in a seri(al)ous race` writeup

- Vulnerability:
  - _Endpoint has a **race condition** vulnerability and **the pickle module is not secure**_
- Where:
  - _`pickle.loads(<note_content>)` endpoint_
- Impact:
  - _Allows to **run commands in the server's shell** by sending commands in notes_

## Steps to reproduce

Before doing the attack, we analyzed the code given `(server3.py)`. When the **Classy** mode is chosen to read, it uses the command `pickle.loads()` which is unsafe:

```python
    if action_choice == '0': # read
        note = pickle.loads(note_content)
        print(note)
```
It is important that when unpickling data, to be sure that it is 100% safe. Since we now know the target, its time to look into how we will going to exploit it.

In the classy mode, when writing the note it will perform the command `pickle.dumps()`, making the `loads` method safe to use later. However, there is an exception. When the note is written in the **Free** mode, it will not use the `dumps` method:

```python
elif action_choice == '1': # write
        with open(note_path, 'wb') as f:
            f.write(note_content.encode('utf8','surrogateescape'))
```
It will directly write in the file that has the **note_path.** This means that we can write a note in the **Free** mode and then read it in the **Classy** mode. This is the vulnerability that we will exploit.

The first thing we need to do is to create a note in the **Free** mode. We will use the following payload:

```python
class shell_access(object):
    def __reduce__(self):
        return (os.system, ('cat /home/ctf/flag', ))

bad_note = pickle.dumps(shell_access())
```
Note that we are using the `os.system` command to execute the `cat /home/ctf/flag` command and pickle it. This, when using the function `loads`, will print the contents of the file flag in the server's shell. It is relevant to say that before this command **we did not know the flag's location**.

To find it, we used the payload with the `find | grep flag` command obtaining the following result:

```bash
[...]
find: '/proc/3551/fdinfo': Permission denied
find: '/proc/3551/ns': Permission denied
find: '/root': Permission denied
/home/ctf/flag
/usr/lib/x86_64-linux-gnu/perl/5.22.1/bits/waitflags.ph
/sys/devices/platform/serial8250/tty/ttyS15/flags
[...]
```
Looking at the result, we can see that there is a file named flag with the path `/home/ctf/flag`, which is probably the flag that we are looking for.

The requests to the server are made in **parallel**. This means that the request to write the note and the request to read it will be made at the same time, having the possibility to read the note right after it is written.

```python
while True:
    Thread(target=partial (writes_script,)).start() 
    read_script()
```

Now, after a few loops, when trying to read the note on **Classy mode** the server will execute the command written on the **note** and it will respond with the content of the `flag`.


## Script
The script used can be found [here](pickles_serialous_race_poc.py)