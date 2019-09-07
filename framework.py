class App:
    def __call__(self, environ, start_response):
        start_response('200 OK', headers=[])
        return [b'<h1>Hello World</h1>']

