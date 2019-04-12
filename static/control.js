const socket = io('/control');

socket.on('playing-users', (data) => {
  console.log("Playing Users: " + data);
  if (data > 1) // Send user back to main
  {
    console.log("Too many players")
    window.location.replace("/");
  }
  document.getElementById("playing-users").innerHTML = data;
});

function button_pressed(action) {
  socket.emit("message", action);
  console.log("button " + action + " pressed");
  console.log(action);
}

function checkPlayingUsers() {
  console.log("Check Playing users...");
  data = document.getElementById("playing-users").innerHTML;
}