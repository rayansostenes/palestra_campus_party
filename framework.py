import wsgiref.headers
import re
from parse import parse

class NotFound(Exception):
    pass

class Request:
    def __init__(self, environ):
        self.environ = environ

    @property
    def path(self):
        return self.environ.get('PATH_INFO')
    
    @property
    def method(self):
        return self.environ.get('REQUEST_METHOD')


class Response:
    def __init__(self, response_body=None, status=200, charset='utf-8', content_type='text/html'):
        self._status = status
        self.charset = charset
        self.content_type = content_type
        self.response_body = response_body.encode('utf-8')
    
        self.headers = wsgiref.headers.Headers()
        self.headers.add_header('content-type', f'{content_type}; charset={charset})')
    
    @property
    def status(self):
        from http.client import responses
        status_string = responses.get(self._status, 'UNKNOWN STATUS')
        return f'{self._status} {status_string}'
    
    def __iter__(self):
        yield self.response_body


def jsonify(data):
    import json
    return Response(json.dumps(data), content_type='application/json')

class App:
    def __init__(self):
        self.routing = []

    def route(self, pattern):
        def wrapper(callback):
            self.routing.append((pattern, callback))
            return callback
        return wrapper

    def match(self, path):
        for pattern, handler in self.routing:
            parse_result = parse(pattern, path)
            if parse_result is not None:
                return handler, parse_result.named
        raise NotFound()

    def __call__(self, environ, start_response):
        try:
            request = Request(environ)
            callback, kwargs = self.match(request.path) 
            response = callback(request, **kwargs)
        except NotFound:
            response = Response('<h1>404 Not Found</h1>', status=404)
        start_response(response.status, response.headers.items())
        return response

