const socket = io('/control');

socket.on('users', (data) => {
  console.log("Playing Users: " + data);
  document.getElementById("playing-users").innerHTML = data;
});

socket.on('force_feedback', (data) => {
  window.navigator.vibrate(200);
  console.log("Force Feedback: " + data);
});

function button_pressed(action) {
  socket.emit("message", action);
  console.log("button " + action + " pressed");
  console.log(action);
}
