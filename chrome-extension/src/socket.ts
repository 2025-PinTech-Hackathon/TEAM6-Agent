// Create WebSocket connection.
export const socket = new WebSocket("ws://127.0.0.1:8000/ws");

// Connection opened
socket.addEventListener("open", () => {
  socket.send("Hello Server!");
});
