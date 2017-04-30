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
`main.py` is the main handler for this app. All settings must be included in `app.yaml` file in order for Google App Engine to recognize & execute your app. Therefore the root domain should execute `main.py` automatically provided you're running within Google App Engine environment.

Live site can be seen at:
[https://joepettigrew-multi-blog.appspot.com/](https://joepettigrew-multi-blog.appspot.com/)


FILE STRUCTURE
----------------
* /main.py - This is the main handler for the app.
* /handlers - All handlers live here.
* /models - All Google Datastore models live here.
* /static - CSS JS live here. includes Bootstrap4 CSS & JS
* /templates - Jinja2 templated HTML files


ADDITIONAL DOCUMENTATION
------------------------
* [Google App Engine SDK Documentation](https://cloud.google.com/appengine/downloads)
* [Google App Engine Python Library](https://cloud.google.com/appengine/docs/standard/python/)
* [Jijna2 Documentation](http://jinja.pocoo.org/docs/2.9/)
* [Webapp2 Documentation](https://webapp2.readthedocs.io/en/latest/)
* [Bootstrap4 Documentation](https://v4-alpha.getbootstrap.com/getting-started/introduction/)


LICENSE
------------------------
The contents of this repository are covered under the [MIT License](LICENSE.md).
