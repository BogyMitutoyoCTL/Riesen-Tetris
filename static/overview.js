const socket = io('/overview');

socket.on('playing-users', (data) => {
  console.log("Playing Users: " + data);
  document.getElementById("playing-users").innerHTML = data;
  if (data > 0) // If there already is someone playing
  {
    document.getElementById('btn-id-tetris').disabled = true;
    console.log("Disable Button Tetris...")
    document.getElementById('btn-id-snake').disabled = true;
    console.log("Disable Button Snake...")
  }
  else
  {
    document.getElementById('btn-id-tetris').disabled = false;
    console.log("Enable Button Tetris...")
    document.getElementById('btn-id-Snake').disabled = false;
    console.log("Enable Button Snake...")
  }
});

socket.on('connected-users', (data) => {
  console.log("Connected Users: " + data);
});

