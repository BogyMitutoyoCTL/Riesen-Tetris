const socket = io('/chose_startscreen');

socket.on('playing-users', (data) => {
  console.log("Playing Users: " + data);
  if (data > 0) // Send user back to main
  {
    console.log("Someone is playing")
    window.location.replace("/");
  }
});

function button_exit_pressed() {
  socket.emit("message", "start_startscreen");
  console.log("exit button pressed, will start the clock");
  window.location.replace("/");
}

function button_pressed(action) {
  socket.emit("message", action);
  console.log("button " + action + " pressed");
  console.log(action);