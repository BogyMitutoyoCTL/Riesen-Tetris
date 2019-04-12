from flask import Flask
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)


@app.route('/post.html', methods=['POST'])
def hello_js():
    return 'post data'


@app.route('/')
def hello():
    return 'main-menu.html'


@app.route('/test.html')
def hello_test():
    html_code = "<!DOCTYPE html><html><body><h1>My Personal Website</h1><p>Hi, this is my personal website.</p></body></html>"
    return html_code


@app.route('/<name>')
def hello_name(name):
    print(name)
    return "Hello {}!".format(name)


@socketio.on('connect', namespace='/control')
def control_connect():
    emit('myresponse', {'data': 'Connected'})


@socketio.on('username', namespace='/control')
def control_username(data):
    print(data)


@socketio.on('myevent', namespace='/control')
def control_myevent(data):
    print('my event')
    print(data)


@socketio.on('disconnect', namespace='/control')
def control_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True, host='0.0.0.0',
                 port=80)
