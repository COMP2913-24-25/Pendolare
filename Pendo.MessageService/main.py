from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Client</title>
    </head>
    <body>
        <h1>WebSocket Client</h1>
        <form action"" onsubmit="sendMessage(event)">
            <input text="text" 


        <button onclick="connectWebSocket()">Connect</button>
        <button onclick="sendMessage()">Send Message</button>
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

            function sendMessage() {
                const message = "Hello from the client!";
                socket.send(message);
            }
        </script>
    </body>
</html>
"""

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received: {data}")
        await websocket.send_text(f"Server received: {data}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
