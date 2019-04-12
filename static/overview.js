const socket = io('/overview');

socket.on('users', (data) => {
  console.log("Playing Users: " + data);
  document.getElementById("playing-users").innerHTML = data;
});
