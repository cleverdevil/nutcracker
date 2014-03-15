from .util import downgrade_wsgi_ux_to_1x, urljoin
from .compat import native_to_unicode

from pecan.core import load_app
from six import add_metaclass, PY3

import abc


@add_metaclass(abc.ABCMeta)
class AppRef(object):
    @abc.abstractproperty
    def app(self):
        raise NotImplemented


class WSGIAppRef(AppRef):
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    @property
    def app(self):
        return self.wsgi_app


class PecanAppRef(AppRef):
    def __init__(self, config_path):
        self.config_path = config_path
        self.pecan_app = load_app(config_path)

    @property
    def app(self):
        return self.pecan_app


class NutcrackerMeta(type):
    def _clean_key(cls, key):
        return '/' if key == '__root__' else '/' + key

    def __init__(cls, name, bases, namespace):
        cls.refs = {
            cls._clean_key(k): v
            for k, v in namespace.items() if isinstance(v, AppRef)
        }
        return super(NutcrackerMeta, cls).__init__(name, bases, namespace)


@add_metaclass(NutcrackerMeta)
class Nutcracker(object):
    def __init__(self):
        self.apps = {path:ref.app for path, ref in self.refs.items()}
        super(Nutcracker, self).__init__()

    def script_name(self, path):
        """
        The script_name of the app at the given path, or None.
        """
        while True:
            if path in self.apps:
                return path

            if path == "":
                return None

            # Move one node up the tree and try again.
            path = path[:path.rfind("/")]

    def __call__(self, environ, start_response):
        env1x = environ
        if environ.get(native_to_unicode('wsgi.version')) == (native_to_unicode('u'), 0):
            env1x = downgrade_wsgi_ux_to_1x(environ)
        path = urljoin(env1x.get('SCRIPT_NAME', ''),
                       env1x.get('PATH_INFO', ''))
        sn = self.script_name(path or "/")
        if sn is None:
            start_response('404 Not Found', [])
            return []

        app = self.apps[sn]

        # Correct the SCRIPT_NAME and PATH_INFO environ entries.
        # Ideally, we would update the SCRIPT_NAME here with the proper
        # value from the app that was mounted
        environ = environ.copy()
        if not PY3:
            if environ.get(native_to_unicode('wsgi.version')) == (native_to_unicode('u'), 0):
                # Python 2/WSGI u.0: all strings MUST be of type unicode
                enc = environ[native_to_unicode('wsgi.url_encoding')]
                environ[native_to_unicode('SCRIPT_NAME')] = sn.decode(enc)
                environ[native_to_unicode('PATH_INFO')] = path[len(sn.rstrip("/")):].decode(enc)
            else:
                # Python 2/WSGI 1.x: all strings MUST be of type str
                environ['SCRIPT_NAME'] = sn
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):]
        else:
            if environ.get(native_to_unicode('wsgi.version')) == (native_to_unicode('u'), 0):
                # Python 3/WSGI u.0: all strings MUST be full unicode
                environ['SCRIPT_NAME'] = sn
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):]
            else:
                # Python 3/WSGI 1.x: all strings MUST be ISO-8859-1 str
                environ['SCRIPT_NAME'] = sn.encode('utf-8').decode('ISO-8859-1')
                environ['PATH_INFO'] = path[len(sn.rstrip("/")):].encode('utf-8').decode('ISO-8859-1')

        return app(environ, start_response)

