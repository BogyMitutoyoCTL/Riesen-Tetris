const socket = io('/control');

socket.on('playing-users', (data) => {
  console.log("Playing Users: " + data);
  if (data > 1) // Send user back to main
  {
    console.log("Too many players")
    window.location.replace("/");
  }
});

function button_pressed(action) {
  socket.emit("message", action);
  console.log("button " + action + " pressed");
  console.log(action);
}

function getUsername() {
    console.log("Get Username...");
    data = document.getElementById("username").value;
    document.getElementById("username-display").innerHTML = data;
    document.getElementById('container-username-id').style.display = 'none'
    socket.emit("message", "tetris_start");
    console.log(data);
}