const socket = io('/overview');

socket.on('playing-users', (data) => {
  console.log("Playing Users: " + data);
  document.getElementById("playing-users").innerHTML = data;
  if (data > 0) // If there already is someone playing
  {
    document.getElementById('btn-id-tetris').disabled = true;
    console.log("Disable Button Tetris...")
  }
  else
  {
    document.getElementById('btn-id-tetris').disabled = false;
    console.log("Enable Button Tetris...")
  }
});

socket.on('connected-users', (data) => {
  console.log("Connected Users: " + data);
});

