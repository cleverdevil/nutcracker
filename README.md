# Nutcracker

Nutcracker allows you to easily create a single WSGI application out of several
[Pecan](http://pecanpy.org) applications or WSGI applications, in a declarative
style familiar to Pecan developers.

## Example

The following application will bind four applications together into a single
application. 

```python
from nutcracker import Nutcracker, PecanAppRef, WSGIAppRef
from my_wsgi_app import app


class MyNutcracker(Nutcracker):
    __root__ = PecanAppRef('/path/to/pecanapp/config.py')
    forums = PecanAppRef('/path/to/pecan/forumapp/config.py')
    blog = PecanAppRef('/path/to/pecan/blogapp/config.py')
    other = WSGIAppRef(app)


from wsgiref.simple_server import make_server
httpd = make_server('', 8123, MyNutcracker())
httpd.serve_forever()
```

## Notes

Nutcracker is based upon Alfredo Deza's 
[pecan-mount](http://github.com/alfredodeza/pecan-mount), but features an API
more acceptable to Pecan developers, less documentation, fewer features, and a
complete gaping void when it comes to tests. Hooray!

My goal is to use this project as a place to play around until a feature worthy
of merging into pecan core emerges. Please help. Please.
