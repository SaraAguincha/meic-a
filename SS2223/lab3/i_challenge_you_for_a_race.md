# Challenge `I challenge you for a race` writeup

- Vulnerability:
  - _Endpoint has a **race condition** vulnerability_
- Where:
  - _`/challenge/flag` endpoint_
- Impact:
  - _Allows to **read the flag** without actually having authorization by using symbolic links_

## Steps to reproduce
Before starting it was required to login using ssh. The following command was used ```ssh username@mustard.stt.rnl.tecnico.ulisboa.pt -p 22651```

After having access to the server, the first thing to do is to create a new folder in the tmp directory. This is done using the command ```mkdir /tmp/<directory_name>```. The folder was created so that only we know its name, making sure that there is no other user that can access it and its contents.

Having our folder created, we need to create a file. Since **we created** it, we will have permissions to read and write to it. This is done using the command ```touch /tmp/<directory_name>/<our_file>```.

Now we can finally start the challenge. The script was written in bash and it does the following:

```bash
while true
do
ln -sf /tmp/ist195674/myfile.txt /tmp/ist195674/goodfile.txt
echo "/tmp/ist195674/goodfile.txt" | /challenge/challenge&
ln -sf /challenge/flag /tmp/ist195674/goodfile.txt
done
```

First, we create a symbolic link to the file `myfile.txt` and name it `goodfile.txt`. Then, we run the challenge with the file `goodfile.txt` as input.
Right after running it, we change the symbolic link to the file `/challenge/flag`. This will make the challenge read the **flag file instead of the goodfile.** Then, the challenge will read the file and print its contents. Since we are running the challenge in a loop, it will keep reading the flag file and printing its contents.

Now, we will be able to read what's in the `flag` file.

## Script
The script used can be found [here](i_challenge_you_for_a_race_poc.sh)
