MULTI USER BLOG
================


ABOUT
----------------
This is a simple blog where multiple users can register to contribute.
The site is written in Python 2.7 and built on Google App Engine using Webapp2 and Jinja2.

REQUIREMENTS
----------------
* Python 2.7
* Google App Engine
* Webapp2
* Jinja2
* Bootstrap 4


INSTRUCTION
----------------
main.py is the main handler for this app. All settings must be included in app.yaml file in order for Google App Engine to recognize & execute your app. Therefore the root domain should execute main.py automatically provided you're running within Google App Engine environment.

Live site can be seen at:
[https://joepettigrew-multi-blog.appspot.com/](https://joepettigrew-multi-blog.appspot.com/)


FILE STRUCTURE
----------------
* main.py - This is the main handler for the app.
* /static - CSS JS live here. includes Bootstrap4 CSS & JS
* /templates - Jinja2 templated HTML files

```
multi-blog
│  README.md
│  app.yaml
|  auth.py
|  datastore.py
|  main.py
|  validate.py    
│
└───static
│   └───css
|   |     bootstrap.min.css
|   |     style.css
|   └───js
│   |     bootstrap.min.js
│   
└───templates
    │  base.html
    │  blogsubmit.html
    │  editpost.html
    │  index.html
    │  login.html
    │  signup.html
    │  singlepost.html
    │  welcome.html
```
