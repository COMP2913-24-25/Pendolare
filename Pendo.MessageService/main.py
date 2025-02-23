from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """ 
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form onsubmit="sendMessage(event); return false;">
            <input type="text" id="messageInput" placeholder="Type a message">
            <button type="button" onclick="connectWebSocket()">Connect</button>
            <button type="submit">Send</button>
        </form>
        <div id="messages"></div>

        <script>
            let socket;

            function connectWebSocket() {
                socket = new WebSocket("ws://localhost:8000/ws");

                socket.onmessage = function(event) {
                    const messages = document.getElementById("messages");
                    messages.innerHTML += `<p>${event.data}</p>`;
                };
            }

            function sendMessage(event) {
                event.preventDefault();

                const input = document.getElementById("messageInput");
                const message = input.value.trim();
                
                if (message && socket && socket.readyState === WebSocket.OPEN) {
                    socket.send(message);

                    // Show sent message in chat
                    const messages = document.getElementById("messages");
                    messages.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

                    input.value = "";  // Clear input after sending
                }
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"You: {data}")  # Send to all connected clients
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
