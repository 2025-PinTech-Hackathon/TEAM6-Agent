// Create WebSocket connection.
export const socket = new WebSocket("ws://localhost:8888/ws/agent");

// Connection opened
socket.addEventListener("open", () => {
  socket.send("Hello Server!");
});
