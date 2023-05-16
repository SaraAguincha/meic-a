# Challenge `Money, money, money!` writeup

- Vulnerability:
  - _Endpoint has a **sql** vulnerability_
- Where:
  - _`/profile` endpoint_
- Impact:
  - _Allows to **change the number of tokens to achieve jackpot** without having the authority to by making a sql injection in the user's bio_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22261`. After the session is established we will need to register and login as a user. It is important to note that every user will have 0 tokens.

After registering and logging in, we can see where the user can change his bio.
The attack will be done by making a sql injection in the bio field. 

It's important to note that when there is a bad login input, the server will return an error message with the following format:

```sql
[SQL:SELECT id, username, password, bio, age, jackpot_val FROM user WHERE username = ''bad_name' AND password = 'potato']
```

From here, we can see that there is a jackpot_val field in the user table. This field is the number of tokens that the user need to have to achieve the jackpot state. We can also conclude that the jackpot_val is set to a random value by default.

Since we don't know what is occurring when submitting the query, we need to make the server give an error message so that we can see it. To do this, we used the following payload:
```sql
' potato
```
Note: every word after the `'` will be considered wrong since it will disrupt the query.

Right after sending, the server returned the following error message:
```sql
[SQL:UPDATE user SET bio = ''potato' WHERE username = '4321']
```

Taking this information into account, we will be taking advantage of the `UPDATE` and update our jackpot_val to `0`. The injection done has the following payload:

```sql
badBio', jackpot_val = '0 
```

By doing this, the user will have its bio updated with the text **badBio** and the jackpot_val will be now **0**.

Now, we have hit the **Jackpot** and can access the secret, getting the `flag`.