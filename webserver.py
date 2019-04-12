import time
from aiohttp import web
import os
import jinja2
import aiohttp_jinja2
import socketio

sio = socketio.AsyncServer(ping_timeout=1, ping_interval=0.2)

app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'
app['name'] = 'CTL WebGameControl v0.1'
app['connect_counter'] = 0

sio.attach(app)


@sio.on('message', namespace='Test')
async def connect_handler():
    print('Message!')


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('control.html')
async def control(request):
    return {}


async def favicon_handler(request):
    return web.FileResponse('./static/favicon.ico')


@sio.on('message', namespace='/control')
async def print_message(sid, message):
    print("Socket ID: ", sid)
    print(message)


@sio.on('connect', namespace='/overview')
async def print_connect_message_overview(sid, message):
    await sio.emit('users', app['connect_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Playing Users: ", app['connect_counter'])


@sio.on('disconnect', namespace='/overview')
async def print_disconnect_message_overview(sid):
    await sio.emit('users', app['connect_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Playing Users: ", app['connect_counter'])


@sio.on('connect', namespace='/control')
async def print_connect_message_control(sid, message):
    app['connect_counter'] = app['connect_counter'] + 1
    await sio.emit('users', app['connect_counter'], namespace='/control')
    await sio.emit('users', app['connect_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Playing Users: ", app['connect_counter'])


@sio.on('disconnect', namespace='/control')
async def print_disconnect_message_control(sid):
    app['connect_counter'] = app['connect_counter']-1
    await sio.emit('users', app['connect_counter'], namespace='/control')
    await sio.emit('users', app['connect_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Playing Users: ", app['connect_counter'])


app.router.add_get('/', index, name='index')
app.router.add_get('/control.html', control, name='control')
app.router.add_get('/favicon.ico', favicon_handler, name='favicon')
app.router.add_static('/static', 'static', name='static')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    web.run_app(app, port=port)
