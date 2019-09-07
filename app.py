from framework import App, Response, jsonify, Request

app = App()

@app.route('/')
def index(request: Request):
    return Response('<h1>Hello Campus Party</h1>')

@app.route('/hello/{name}')
def hello(name):
    return Response(f'<h1>Hello, {name} </h1>')

@app.route('/json')
def hello():
    return jsonify({
        'hello': 'World',
    })

application = app