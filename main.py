from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

app = FastAPI(
    title="Vercel + FastAPI CCTV & Tracker",
    description="Camera Connection and Real-time Location Tracking API",
    version="1.0.0",
)

# --- IN-MEMORY DATABASE (Temporary Storage for Vercel Serverless) ---
cameras_db = {
    "cam-01": {
        "id": "cam-01", 
        "name": "Main Gate Camera", 
        "status": "online", 
        "stream_url": "https://sample.vodobox.net/skate_phantom_flex_4k/skate_phantom_flex_4k.m3u8", 
        "updated_at": datetime.now().isoformat()
    }
}

locations_db = {
    "loc-01": {
        "id": "loc-01", 
        "username": "Rohan_Sharma", 
        "latitude": 28.6139, 
        "longitude": 77.2090, 
        "updated_at": datetime.now().isoformat()
    }
}


# --- PYDANTIC MODELS FOR VALIDATION ---
class CameraConnectModel(BaseModel):
    id: str
    name: str
    status: str = "online"
    stream_url: Optional[str] = None

class LocationUpdateModel(BaseModel):
    id: str
    username: str
    latitude: float
    longitude: float


# ==========================================
# FEATURE 1: CAMERA / CCTV ENDPOINTS
# ==========================================

# 1. Camera Access Point - App ya Device ko connect karne ke liye
@app.post("/camera", tags=["Camera"])
def connect_camera(camera: CameraConnectModel):
    cameras_db[camera.id] = {
        "id": camera.id,
        "name": camera.name,
        "status": camera.status,
        "stream_url": camera.stream_url or f"http://local-stream-ip/live/{camera.id}",
        "updated_at": datetime.now().isoformat()
    }
    return {"status": "success", "message": "Camera access established successfully", "data": cameras_db[camera.id]}


# 2. Camera Info & Live Status - Saare connections aur status manage karne ke liye
@app.get("/camera/info", tags=["Camera"])
def get_all_cameras_info():
    total_cameras = len(cameras_db)
    online_count = sum(1 for cam in cameras_db.values() if cam["status"] == "online")
    
    return {
        "total_managed_cameras": total_cameras,
        "live_online_count": online_count,
        "connections": list(cameras_db.values())
    }


# 3. View Live CCTV by ID - Specific camera ka live access lene ke liye
@app.get("/camera/{camera_id}", tags=["Camera"])
def get_live_camera(camera_id: str):
    if camera_id not in cameras_db:
        raise HTTPException(status_code=404, detail=f"Camera with ID '{camera_id}' not found.")
    
    camera_data = cameras_db[camera_id]
    return {
        "camera_id": camera_data["id"],
        "name": camera_data["name"],
        "connection_status": camera_data["status"],
        "live_stream_url": camera_data["stream_url"],
        "instruction": "Embed this stream_url into your app player to watch live CCTV."
    }


# ==========================================
# FEATURE 2: REAL-TIME LOCATION ENDPOINTS
# ==========================================

# 1. Post Real-Time Location - User ki real-time location capture karne ke liye
@app.post("/location", tags=["Location"])
def update_user_location(location: LocationUpdateModel):
    locations_db[location.id] = {
        "id": location.id,
        "username": location.username,
        "latitude": location.latitude,
        "longitude": location.longitude,
        "updated_at": datetime.now().isoformat()
    }
    return {"status": "success", "message": "Real-time location captured", "data": locations_db[location.id]}


# 2. Location Info & Management - Pure tracking system ka status dashboard
@app.get("/location-info", tags=["Location"])
def get_location_system_info():
    return {
        "system_status": "Active",
        "total_tracked_devices": len(locations_db),
        "all_tracked_locations": list(locations_db.values())
    }


# 3. View Location by ID - Kisi specific user/device ki location dekhne ke liye
@app.get("/location/{location_id}", tags=["Location"])
def get_location_by_id(location_id: str):
    if location_id not in locations_db:
        raise HTTPException(status_code=404, detail=f"Location record '{location_id}' not found.")
    return locations_db[location_id]


# ==========================================
# HOME PAGE HTML RESPONSE
# ==========================================
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FastAPI CCTV & Tracker Hub</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, system-ui, sans-serif; background-color: #000; color: #fff; min-height: 100vh; display: flex; flex-direction: column; }
            nav { max-width: 1200px; margin: 0 auto; display: flex; align-items: center; padding: 1.5rem 2rem; width: 100%; border-bottom: 1px solid #222; }
            .logo { font-size: 1.25rem; font-weight: 700; color: #fff; text-decoration: none; }
            .nav-links { margin-left: auto; display: flex; gap: 1rem; }
            .nav-links a { color: #888; text-decoration: none; font-size: 0.9rem; padding: 0.5rem 1rem; border-radius: 6px; transition: 0.2s; }
            .nav-links a:hover { color: #fff; background: #111; }
            main { flex: 1; max-width: 1200px; margin: 0 auto; padding: 3rem 2rem; text-align: center; width: 100%; }
            h1 { font-size: 2.5rem; margin-bottom: 0.5rem; background: linear-gradient(to right, #fff, #666); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
            p.subtitle { color: #888; margin-bottom: 3rem; }
            .cards { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; }
            .card { background: #111; border: 1px solid #222; border-radius: 12px; padding: 1.5rem; text-align: left; transition: 0.2s; }
            .card:hover { border-color: #444; transform: translateY(-2px); }
            .card h3 { font-size: 1.1rem; margin-bottom: 0.5rem; color: #00ff88; }
            .card p { color: #888; font-size: 0.85rem; margin-bottom: 1.5rem; line-height: 1.4; }
            .card a { display: block; text-align: center; color: #fff; background: #222; text-decoration: none; font-size: 0.85rem; font-weight: 600; padding: 0.6rem; border-radius: 6px; border: 1px solid #333; }
            .card a:hover { background: #333; }
            .badge { display: inline-flex; align-items: center; gap: 0.4rem; background: #0070f3; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.75rem; margin-bottom: 1.5rem; }
            .dot { width: 6px; height: 6px; background: #00ff88; border-radius: 50%; }
        </style>
    </head>
    <body>
        <nav>
            <a href="/" class="logo">📡 CCTV & Tracker Hub</a>
            <div class="nav-links">
                <a href="/docs" target="_blank">Interactive Docs UI</a>
                <a href="/camera/info">Live Camera Info</a>
                <a href="/location-info">Tracker Dashboard</a>
            </div>
        </nav>
        <main>
            <div class="badge"><span class="dot"></span> Systems Fully Operational</div>
            <h1>FastAPI + Vercel Dashboard</h1>
            <p class="subtitle">API endpoints for managing smart CCTV feeds and real-time user location tracking.</p>
            
            <div class="cards">
                <div class="card">
                    <h3>📷 Swagger API Docs</h3>
                    <p>Open the interactive UI to test real-time POST requests, view schemas, and query endpoints live.</p>
                    <a href="/docs" target="_blank">Open Swagger UI →</a>
                </div>
                <div class="card">
                    <h3>📹 CCTV Live Status</h3>
                    <p>Check current network stream status, manage access points, and verify device health.</p>
                    <a href="/camera/info">View Camera Info →</a>
                </div>
                <div class="card">
                    <h3>📍 Location Analytics</h3>
                    <p>Access geo-coordinates tracking logs, active users, and manage live GPS feed incoming points.</p>
                    <a href="/location-info">View Location Logs →</a>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
