from flask import Flask

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True, host='0.0.0.0', port=80)
