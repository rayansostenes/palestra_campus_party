from framework import App, Response

app = App()

@app.route(r'^/$')
def index(request):
    return Response('<h1>Hello Campus Party</h1>')

@app.route(r'^/hello/(\w+)$')
def hello(request, name):
    return Response(f'<h1>Hello, {name} </h1>')

application = app