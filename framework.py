import wsgiref.headers

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


class App:
    def __call__(self, environ, start_response):
        request = Request(environ)
        response = Response('<h1>Hello World</h1>')
        start_response(response.status, headers=response.headers.items())
        return response

