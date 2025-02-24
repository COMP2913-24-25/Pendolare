from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
import json


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
            let username = prompt("Enter your name:");

            function connectWebSocket() {
                socket = new WebSocket("ws://localhost:8000/ws");

                socket.onopen = function () {
                    socket.send(JSON.stringify({ type: "connect", username: username }));
                };

                socket.onmessage = function (event) {
                    const data = JSON.parse(event.data);
                    const messages = document.getElementById("messages");

                    if (data.type === "message") {
                        let senderName = data.sender === username ? "You" : data.sender;
                        messages.innerHTML += `<p><strong>${senderName}:</strong> ${data.message}</p>`;
        }
                };
            }


            function sendMessage(event) {
                event.preventDefault();

                const input = document.getElementById("messageInput");
                const message = input.value.trim();

                if (message && socket && socket.readyState === WebSocket.OPEN) {
                    socket.send(JSON.stringify({ type: "message", message: message }));

                    // Show sent message in chat
                    //const messages = document.getElementById("messages");
                    //messages.innerHTML += `<p><strong>You:</strong> ${message}</p>`;

                    input.value = "";
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
        self.active_connections: dict[WebSocket, str] = {}  # Store WebSocket -> username mapping

    async def connect(self, websocket: WebSocket):
        await websocket.accept()

    def register(self, websocket: WebSocket, username: str):
        self.active_connections[websocket] = username  # Store the username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            del self.active_connections[websocket]

    async def broadcast(self, message: str, sender_ws: WebSocket):
        sender_name = self.active_connections.get(sender_ws, "Unknown")
        data = json.dumps({"type": "message", "sender": sender_name, "message": message})

        for connection in self.active_connections.keys():
            await connection.send_text(data)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)

            if data["type"] == "connect":
                manager.register(websocket, data["username"])
            elif data["type"] == "message":
                await manager.broadcast(data["message"], websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
