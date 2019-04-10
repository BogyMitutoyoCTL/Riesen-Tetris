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
turnL.onclick = alert('Halt STOP!');
    WebSocket.send(JSON.stringify({action= 'turnL'}));

turnR.onclick = function(event) {
    WebSocket.send(JSON.stringify({action= 'turnR'}));
}
down.onclick = function(event) {
    WebSocket.send(JSON.stringify({action= 'down'}));
}




