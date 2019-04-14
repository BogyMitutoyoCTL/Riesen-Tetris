import time

import redis
from aiohttp import web
import json
import os
import jinja2
import aiohttp_jinja2
import socketio

from highscorelist import Highscorelist

r = redis.StrictRedis(host='localhost', port=6379)

sio = socketio.AsyncServer(ping_timeout=1, ping_interval=0.2)

app = web.Application()

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'
app['name'] = 'CTL WebGameControl v0.1'
app['connect_counter'] = 0
app['playing_counter'] = 0
app['highscores'] = json.loads(json.dumps(
    {'1': {'name': 'Name1', 'point': 201, 'date': "1 - 20 - 2019"}, '2': {'name': 'Name2', 'point': 202, 'date': "2- 20 - 2019"}}))

sio.attach(app)


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


@aiohttp_jinja2.template('control.html')
async def control(request):
    return {}


@aiohttp_jinja2.template('highscores.html')
async def highscores(request):
    # return json.dumps({{'point': 20, 'name': "TW", 'date': '2019-02-11'}})
    r = {'1': {'point': 20, 'name': "TW", 'date': '2019-02-11'}, '2': {'point': 20, 'name': "TW", 'date': '2019-02-11'}}

    x = Highscorelist('Tetris')
    x.load()
    print(x.highscores)
    v = {}
    amount_of_entrys = 0
    for i in range(len(x.highscores)):
        v[str(i)] = {'point':x.highscores[i].point, 'name':x.highscores[i].name,
                'date':str(x.highscores[i].date.strftime("%d.%m.%y"))}
        amount_of_entrys = i+1
    print(v[str(0)])
    app['amount_of_highscores'] = amount_of_entrys

    r = json.dumps(v)
    loaded_r = json.loads(r)

    app['highscores'] = v
    return {}


@aiohttp_jinja2.template('control_snake.html')
async def control_snake(request):
    return {}


@aiohttp_jinja2.template('chose_startscreen.html')
async def chose_startscreen(request):
    return {}


async def favicon_handler(request):
    return web.FileResponse('./static/favicon.ico')


@sio.on('username', namespace='/control')
async def print_message(sid, message):
    r.publish('username', message)
    print("Socket ID: ", sid)
    print("Username: " + message)


@sio.on('message', namespace='/control')
async def print_message(sid, message):
    r.publish('game_action', message)
    print("Socket ID: ", sid)
    print(message)


@sio.on('username', namespace='/control_snake')
async def print_message(sid, message):
    r.publish('username', message)
    print("Socket ID: ", sid)
    print("Username: " + message)


@sio.on('message', namespace='/control_snake')
async def print_message(sid, message):
    r.publish('game_action', message)
    print("Socket ID: ", sid)
    print(message)


@sio.on('message', namespace='/chose_startscreen')
async def print_message(sid, message):
    r.publish('game_action', message)
    print("Socket ID: ", sid)
    print(message)


@sio.on('connect', namespace='/overview')
async def print_connect_message_overview(sid, message):
    app['connect_counter'] += 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Connected Users: ", app['connect_counter'])
    print("Playing Users: ", app['playing_counter'])


@sio.on('disconnect', namespace='/overview')
async def print_disconnect_message_overview(sid):
    app['connect_counter'] -= 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Connected Users: ", app['connect_counter'])
    print("Playing Users: ", app['playing_counter'])


@sio.on('connect', namespace='/control')
async def print_connect_message_control(sid, message):
    app['connect_counter'] += 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] += 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/control')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


@sio.on('disconnect', namespace='/control')
async def print_disconnect_message_control(sid):
    app['connect_counter'] -= 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] -= 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/control')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


@sio.on('connect', namespace='/control_snake')
async def print_connect_message_control_snake(sid, message):
    app['connect_counter'] += 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] += 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/control_snake')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


@sio.on('disconnect', namespace='/control_snake')
async def print_disconnect_message_control_snake(sid):
    app['connect_counter'] -= 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] -= 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/control_snake')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


@sio.on('connect', namespace='/chose_startscreen')
async def print_connect_message_chose_startscreen(sid, message):
    print("connected")
    app['connect_counter'] += 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] += 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/chose_startscreen')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Connect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


@sio.on('disconnect', namespace='/chose_startscreen')
async def print_disconnect_message_chose_startscreen(sid):
    app['connect_counter'] -= 1
    await sio.emit('connected-users', app['connect_counter'], namespace='/overview')
    app['playing_counter'] -= 1
    await sio.emit('playing-users', app['playing_counter'], namespace='/chose_startscreen')
    await sio.emit('playing-users', app['playing_counter'], namespace='/overview')
    print("Disconnect Socket ID: ", sid)
    print("Playing Users: ", app['playing_counter'])


app.router.add_get('/', index, name='index')
app.router.add_get('/control.html', control, name='control')
app.router.add_get('/highscores.html', highscores, name='highscores')
app.router.add_get('/control_snake.html', control_snake, name='control_snake')
app.router.add_get('/chose_startscreen.html', chose_startscreen, name='chose_startscreen')
app.router.add_get('/favicon.ico', favicon_handler, name='favicon')
app.router.add_static('/static', 'static', name='static')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 80))
    web.run_app(app, port=port)
