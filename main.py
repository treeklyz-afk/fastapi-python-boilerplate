from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List
import json
import asyncio

app = FastAPI(
    title="CCTV Stream & Control Server",
    description="Real-time WebSocket server for Android Camera Stream and Tracking",
    version="2.0.0"
)

# --- CONNECTION MANAGER FOR APPS & VIEWERS ---
class ConnectionManager:
    def __init__(self):
        # active_cameras: { camera_id: WebSocket_of_Android_App }
        self.active_cameras: Dict[str, WebSocket] = {}
        # viewers: { camera_id: [List_of_Viewer_WebSockets] }
        self.viewers: Dict[str, List[WebSocket]] = {}
        # metadata: { camera_id: { "model": ..., "status": ... } }
        self.camera_metadata: Dict[str, dict] = {}

    async def register_camera(self, camera_id: str, websocket: WebSocket, model: str):
        self.active_cameras[camera_id] = websocket
        self.camera_metadata[camera_id] = {
            "id": camera_id,
            "device_model": model,
            "status": "online"
        }
        if camera_id rebellion not in self.viewers:
            self.viewers[camera_id] = []
        print(f"📷 Camera Registered: {camera_id} ({model})")

    def disconnect_camera(self, camera_id: str):
        if camera_id in self.active_cameras:
            del self.active_cameras[camera_id]
        if camera_id in self.camera_metadata:
            self.camera_metadata[camera_id]["status"] = "offline"
        print(f"❌ Camera Disconnected: {camera_id}")

    async def register_viewer(self, camera_id: str, websocket: WebSocket):
        if camera_id not in self.viewers:
            self.viewers[camera_id] = []
        self.viewers[camera_id].append(websocket)
        print(f"👀 New Viewer added for Camera: {camera_id}")

    def disconnect_viewer(self, camera_id: str, websocket: WebSocket):
        if camera_id in self.viewers and websocket in self.viewers[camera_id]:
            self.viewers[camera_id].remove(websocket)
            print(f"👀 Viewer disconnected from Camera: {camera_id}")

    async def broadcast_frame(self, camera_id: str, frame_bytes: bytes):
        if camera_id in self.viewers:
            disconnected_viewers = []
            for viewer in self.viewers[camera_id]:
                try:
                    await viewer.send_bytes(frame_bytes)
                except Exception:
                    disconnected_viewers.append(viewer)
            
            for v in disconnected_viewers:
                self.disconnect_viewer(camera_id, v)

    async def send_command(self, camera_id: str, command: dict):
        if camera_id in self.active_cameras:
            app_ws = self.active_cameras[camera_id]
            await app_ws.send_text(json.dumps(command))
            return True
        return False

manager = ConnectionManager()


# ==========================================
# 1. ANDROID APP CONNECTION ENDPOINT (WebSocket)
# ==========================================
@app.websocket("/ws")
async def android_app_websocket(websocket: WebSocket):
    await websocket.accept()
    camera_id = None
    try:
        # First Packet standard authentication routine handle karein
        first_msg = await websocket.receive_text()
        data = json.loads(first_msg)
        
        if data.get("type") == "register_app":
            auth_key = data.get("authKey", "NONE")
            model = data.get("deviceModel", "UNKNOWN")
            
            # Agar auth key 'NONE' hai toh default fallback device model ko bana lein
            camera_id = auth_key if auth_key != "NONE" else model
            await manager.register_camera(camera_id, websocket, model)
            
            # Auto start instruction send karein connect hote hi
            await manager.send_command(camera_id, {"action": "START_CAM", "cameraFacing": "BACK"})
        else:
            await websocket.close(code=4003, reason="Auth failed")
            return

        # Continuous Frame Receiver Loop
        while True:
            # Android app se direct byte frames receive honge
            frame_bytes = await websocket.receive_bytes()
            # Un bytes ko active web viewers tak turant forward karein
            await manager.broadcast_frame(camera_id, frame_bytes)

    except WebSocketDisconnect:
        if camera_id:
            manager.disconnect_camera(camera_id)
    except Exception as e:
        print(f"Error in App WebSocket: {e}")
        if camera_id:
            manager.disconnect_camera(camera_id)


# ==========================================
# 2. WEB VIEWERS STREAM ENDPOINT (WebSocket)
# ==========================================
@app.websocket("/ws/viewer/{camera_id}")
async def web_viewer_websocket(websocket: WebSocket, camera_id: str):
    await websocket.accept()
    await manager.register_viewer(camera_id, websocket)
    try:
        while True:
            # Client connection alive rakhne ke liye ping-pong listener
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect_viewer(camera_id, websocket)


# ==========================================
# 3. LIVE STREAM DASHBOARD (HTML UI)
# ==========================================
@app.get("/camera/{camera_id}", response_class=HTMLResponse)
async def view_live_camera(camera_id: str):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live CCTV Feed - {camera_id}</title>
        <style>
            body {{ font-family: sans-serif; background: #0a0a0a; color: #fff; text-align: center; padding: 20px; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #111; padding: 20px; border-radius: 12px; border: 1px solid #333; }}
            img {{ width: 100%; max-height: 450px; background: #000; border-radius: 8px; margin-top: 15px; border: 1px solid #444; }}
            .btn {{ display: inline-block; padding: 10px 20px; margin: 10px 5px; background: #222; color: #fff; border: 1px solid #444; cursor: pointer; border-radius: 6px; font-weight: bold; text-decoration: none; }}
            .btn:hover {{ background: #333; }}
            .btn-start {{ border-color: #00ff88; color: #00ff88; }}
            .btn-stop {{ border-color: #ff3333; color: #ff3333; }}
            .status {{ font-size: 14px; color: #888; margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>📷 Live CCTV Master Feed</h2>
            <div class="status">Device Target ID: <b>{camera_id}</b></div>
            
            <div id="connection-status" style="color: #ffcc00;">Connecting to Server Tunnel...</div>
            
            <img id="live-stream" src="" alt="Waiting for live frame transmission..." />
            
            <br/><br/>
            <div>
                <button class="btn btn-start" onclick="controlCam('START_CAM')">Turn Camera ON</button>
                <button class="btn btn-stop" onclick="controlCam('STOP_CAM')">Turn Camera OFF</button>
            </div>
            <a href="/camera/info" class="btn">📊 View Network Info</a>
        </div>

        <script>
            const camera_id = "{camera_id}";
            const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
            const wsUrl = protocol + "//" + window.location.host + "/ws/viewer/" + camera_id;
            
            const ws = new WebSocket(wsUrl);
            const imgElement = document.getElementById("live-stream");
            const statusElement = document.getElementById("connection-status");

            ws.onopen = () => {{
                statusElement.innerText = "⚡ Connection Active - Receiving Stream Data";
                statusElement.style.color = "#00ff88";
            }};

            ws.onmessage = (event) => {{
                // Blob conversion optimization for clean memory management
                const blob = event.data;
                const oldUrl = imgElement.src;
                imgElement.src = URL.createObjectURL(blob);
                if (oldUrl.startsWith("blob:")) {{
                    URL.revokeObjectURL(oldUrl); // Memory leak protection
                }}
            }};

            ws.onclose = () => {{
                statusElement.innerText = "❌ Stream Offline / Disconnected";
                statusElement.style.color = "#ff3333";
            }};

            async function controlCam(actionName) {{
                // Trigger camera trigger state API directly
                await fetch(`/api/control/${camera_id}?action=${{actionName}}`, {{method: 'POST'}});
            }}
        </script>
    </body>
    </html>
    """


# ==========================================
# 4. REMOTE CONTROL & METADATA ENDPOINTS
# ==========================================
@app.post("/api/control/{camera_id}", tags=["Management"])
async def trigger_camera_action(camera_id: str, action: str):
    """Viewers yahan se START_CAM ya STOP_CAM commands push kar sakte hain app ko"""
    if action not in ["START_CAM", "STOP_CAM"]:
        raise HTTPException(status_code=400, detail="Invalid Action Parameter.")
    
    payload = {"action": action, "cameraFacing": "BACK"}
    success = await manager.send_command(camera_id, payload)
    
    if success:
        return {"status": "success", "message": f"Command {action} transmitted successfully."}
    raise HTTPException(status_code=404, detail="Target camera node is offline or un-registered.")


@app.get("/camera/info", tags=["Management"])
def get_all_managed_devices():
    """App me dynamic status ya logs dekhne ke liye endpoint"""
    return {
        "active_device_count": len(manager.active_cameras),
        "devices_registry": list(manager.camera_metadata.values())
    }
