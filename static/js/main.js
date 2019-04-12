namespace = '/control';

var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

$(document).ready(function() {

            socket.on('connect', function() {
                socket.emit('myevent', {data: 'I\'m connected!'});
            });

            socket.on('myresponse', function(msg) {
                console.log(msg);

            });
            });
function handleClick(event) {
    socket.emit('username', "Ich bin der User")
             }





/*
const right = document.querySelector('#right');
const left = document.querySelector('#left');
const turnL = document.querySelector('#turnL');
const turnR = document.querySelector('#turnR');
const down = document.querySelector('.down');
const ws = new WebSocket("ws://websocket.org")

right.onclick = function(event) {
    WebSocket.send(JSON.stringify({action: 'right'}));
}
left.onclick = function(event) {
    WebSocket.send(JSON.stringify({action= 'left'}));
}
turnL.onclick = function(event);
    WebSocket.send(JSON.stringify({action= 'turnL'}));

turnR.onclick = function(event) {
    WebSocket.send(JSON.stringify({action= 'turnR'}));
}
down.onclick = function(event) {
    WebSocket.send(JSON.stringify({action= 'down'}));
}
*/




