from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import urllib.parse

app = FastAPI(
    title="⚡ CyberShop 3D Engine + Payment Mesh",
    description="Next-Gen E-Commerce Storefront with Embedded Multiple Gateway Routing",
    version="3.0.0"
)

# --- IN-MEMORY DATABASE STATES ---
products_db = [
    {
        "id": 1,
        "name": "Wireless AirBuds Pro",
        "price": 2999.0,
        "description": "Active noise cancellation with extra deep holographic bass, tactile sensory nodes, and 30hrs runtime.",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"
    },
    {
        "id": 2,
        "name": "AMOLED Cyber Watch",
        "price": 4499.0,
        "description": "Always-on quantum sync layer, biometric radar tracker, customized widget modules, and tactile metallic chassis.",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&q=80"
    },
    {
        "id": 3,
        "name": "Stealth Leather Armor Wallet",
        "price": 999.0,
        "description": "Aerospace grade RFID defense nodes bound inside premium full-grain leather architecture geometry.",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&q=80"
    }
]

# Multiple Custom Gateway Switcher Database
payment_config = {
    "active_method": "upi_intent", # upi_intent, phonepe_merchant, static_qr
    "upi_id": "paytm@upi",
    "merchant_name": "CyberShop Digital",
    "phonepe_merchant_id": "MID987654321",
    "static_qr_url": "https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg"
}

transactions_db = []


# --- PYDANTIC SCHEMAS ---
class ProductModel(BaseModel):
    name: str
    price: float
    description: str
    image_url: str

class PaymentConfigModel(BaseModel):
    active_method: str
    upi_id: Optional[str] = ""
    merchant_name: Optional[str] = ""
    phonepe_merchant_id: Optional[str] = ""
    static_qr_url: Optional[str] = ""


# ==========================================
# CORE PRODUCTS & CORE GATEWAY APIs
# ==========================================
@app.get("/api/products")
def get_all_products():
    return products_db

@app.post("/api/products")
def add_new_product(product: ProductModel):
    new_id = max([p["id"] for p in products_db], default=0) + 1
    product_dict = {"id": new_id, **product.model_dump()}
    products_db.append(product_dict)
    return {"status": "success", "product": product_dict}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    global products_db
    products_db = [p for p in products_db if p["id"] != product_id]
    return {"status": "success"}

@app.get("/api/payment/config")
def get_payment_config():
    return payment_config

@app.post("/api/payment/config")
def update_payment_config(config: PaymentConfigModel):
    global payment_config
    payment_config.update(config.model_dump(exclude_unset=True))
    return {"status": "success", "message": "Gateway configuration route mutated safely.", "current": payment_config}


# ==========================================
# CORE THEME WRAPPER ARCHITECTURE (iOS UI)
# ==========================================
def get_shared_layout(content: str, active_tab: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en" class="scroll-smooth">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
        <title>⚡ CyberShop Premium Matrix</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: radial-gradient(circle at 50% 0%, #170f2b 0%, #08050e 80%, #010003 100%); }}
            .glass-card {{ background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(25px); -webkit-backdrop-filter: blur(25px); border: 1px solid rgba(255, 255, 255, 0.08); }}
            .neon-border-green {{ border-color: rgba(0, 255, 170, 0.2); }}
            .neon-border-green:hover {{ border-color: rgba(0, 255, 170, 0.5); box-shadow: 0 0 25px rgba(0, 255, 170, 0.15); }}
        </style>
    </head>
    <body class="text-gray-100 min-h-screen flex flex-col pb-24 md:pb-0">
        <nav class="bg-black/40 backdrop-blur-md sticky top-0 z-50 px-6 py-4 border-b border-white/5">
            <div class="max-w-5xl mx-auto flex justify-between items-center">
                <a href="/" class="text-xl font-black tracking-tighter bg-gradient-to-r from-cyan-400 via-emerald-400 to-purple-500 bg-clip-text text-transparent flex items-center gap-2">
                    <i class="fas fa-microchip"></i> CYBER✕SHOP
                </a>
                <div class="hidden md:flex space-x-1 bg-white/5 p-1 rounded-full border border-white/10">
                    <a href="/" class="px-5 py-1.5 rounded-full text-xs font-bold transition {"bg-emerald-500 text-gray-950 shadow-md" if active_tab == 'home' else "text-gray-400 hover:text-white"}">Catalog</a>
                    <a href="/admin" class="px-5 py-1.5 rounded-full text-xs font-bold transition {"bg-emerald-500 text-gray-950 shadow-md" if active_tab == 'admin' else "text-gray-400 hover:text-white"}">Terminal</a>
                    <a href="/pay" class="px-5 py-1.5 rounded-full text-xs font-bold transition {"bg-emerald-500 text-gray-950 shadow-md" if active_tab == 'pay' else "text-gray-400 hover:text-white"}">Gateway Engine</a>
                    <a href="/settings" class="px-5 py-1.5 rounded-full text-xs font-bold transition {"bg-emerald-500 text-gray-950 shadow-md" if active_tab == 'settings' else "text-gray-400 hover:text-white"}">Config</a>
                </div>
            </div>
        </nav>
        <main class="flex-1 max-w-5xl w-full mx-auto p-4 md:p-6">{content}</main>
        
        <div class="md:hidden fixed bottom-6 left-4 right-4 bg-black/60 backdrop-blur-2xl border border-white/10 rounded-2xl flex justify-around py-3 z-50 shadow-2xl">
            <a href="/" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'home' else "text-gray-400"}"><i class="fas fa-border-all text-lg"></i><span class="text-[9px] font-bold mt-1 uppercase">Shop</span></a>
            <a href="/admin" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'admin' else "text-gray-400"}"><i class="fas fa-server text-lg"></i><span class="text-[9px] font-bold mt-1 uppercase">Admin</span></a>
            <a href="/pay" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'pay' else "text-gray-400"}"><i class="fas fa-wallet text-lg"></i><span class="text-[9px] font-bold mt-1 uppercase">Pay Setup</span></a>
            <a href="/settings" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'settings' else "text-gray-400"}"><i class="fas fa-sliders text-lg"></i><span class="text-[9px] font-bold mt-1 uppercase">Config</span></a>
        </div>
    </body>
    </html>
    """


# ==========================================
# MODULE ROUTE 1: STORE DECK & INVENTORY VIEW
# ==========================================
@app.get("/", response_class=HTMLResponse)
def page_storefront():
    content = """
    <div class="mb-6 flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-black text-white tracking-tight">AVAILABLE MATRIX STORAGE</h1>
            <p class="text-gray-400 text-xs">Tap any tactical deck element to evaluate custom product architecture data</p>
        </div>
    </div>
    <div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6"></div>

    <script>
        async function renderCatalog() {
            const res = await fetch('/api/products');
            const products = await res.json();
            const grid = document.getElementById('product-grid');
            grid.innerHTML = '';
            products.forEach(p => {
                grid.innerHTML += `
                    <div class="glass-card neon-border-green rounded-2xl overflow-hidden transition-all duration-300 flex flex-col justify-between group">
                        <div class="relative aspect-video w-full bg-black/40 overflow-hidden">
                            <img src="${p.image_url}" class="w-full h-full object-cover group-hover:scale-105 transition duration-500" />
                        </div>
                        <div class="p-4 flex-1 flex flex-col justify-between">
                            <div>
                                <h3 class="font-extrabold text-lg text-white mb-1">${p.name}</h3>
                                <p class="text-gray-400 text-xs line-clamp-2">${p.description}</p>
                            </div>
                            <div class="flex items-center justify-between mt-5 pt-3 border-t border-white/5">
                                <span class="text-xl font-black text-emerald-400">₹${p.price}</span>
                                <div class="flex gap-2">
                                    <a href="/product/${p.id}" class="bg-white/5 hover:bg-white/10 text-white font-bold text-xs px-3 py-2 rounded-xl transition border border-white/10">Details</a>
                                    <a href="/checkout/${p.id}" class="bg-gradient-to-r from-emerald-400 to-cyan-500 hover:brightness-110 text-gray-950 font-extrabold text-xs px-4 py-2 rounded-xl shadow-md transition">Acquire</a>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        window.onload = renderCatalog;
    </script>
    """
    return get_shared_layout(content, "home")


# ==========================================
# MODULE ROUTE 2: DYNAMIC PRODUCT DETAILS PAGE
# ==========================================
@app.get("/product/{product_id}", response_class=HTMLResponse)
def page_product_detail(product_id: int):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        return RedirectResponse("/")
    
    content = f"""
    <a href="/" class="text-xs font-bold text-emerald-400 mb-4 inline-flex items-center gap-1 hover:underline"><i class="fas fa-arrow-left"></i> Back to Deck Inventory</a>
    <div class="glass-card rounded-3xl overflow-hidden grid grid-cols-1 md:grid-cols-2 gap-6 p-6 mt-2 shadow-2xl">
        <div class="rounded-2xl overflow-hidden border border-white/10 bg-black/50 aspect-square">
            <img src="{product['image_url']}" class="w-full h-full object-cover" />
        </div>
        <div class="flex flex-col justify-between py-2">
            <div>
                <span class="bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 px-3 py-1 rounded-full text-[10px] tracking-widest font-mono uppercase font-bold">Secure Hardware Payload</span>
                <h1 class="text-3xl font-black text-white tracking-tight mt-3 mb-2">{product['name']}</h1>
                <p class="text-gray-300 text-sm leading-relaxed font-medium">{product['description']}</p>
                
                <div class="grid grid-cols-2 gap-3 mt-6">
                    <div class="bg-white/5 border border-white/5 p-3 rounded-xl">
                        <span class="text-[9px] text-gray-500 uppercase font-black block tracking-wider">Node Encrypted</span>
                        <span class="text-gray-200 font-bold text-xs mt-0.5 block">AES-256 Quantum</span>
                    </div>
                    <div class="bg-white/5 border border-white/5 p-3 rounded-xl">
                        <span class="text-[9px] text-gray-500 uppercase font-black block tracking-wider">Deployment Path</span>
                        <span class="text-emerald-400 font-bold text-xs mt-0.5 block">Instant Link Sync</span>
                    </div>
                </div>
            </div>
            
            <div class="pt-6 border-t border-white/5 mt-6 flex items-center justify-between">
                <div class="flex flex-col">
                    <span class="text-[9px] text-gray-500 uppercase font-bold tracking-widest">Calculated Core Value</span>
                    <span class="text-3xl font-black text-emerald-400">₹{product['price']}</span>
                </div>
                <a href="/checkout/{product['id']}" class="bg-gradient-to-r from-emerald-400 to-cyan-500 hover:brightness-110 text-gray-950 font-black text-sm px-6 py-3.5 rounded-xl shadow-lg shadow-emerald-500/10 transition">
                    PROCEED TO SECURE CHECKOUT
                </a>
            </div>
        </div>
    </div>
    """
    return get_shared_layout(content, "home")


# ==========================================
# MODULE ROUTE 3: DYNAMIC PREMIUM CHECKOUT PAGE
# ==========================================
@app.get("/checkout/{product_id}", response_class=HTMLResponse)
def page_checkout(product_id: int):
    product = next((p for p in products_db if p["id"] == product_id), None)
    if not product:
        return RedirectResponse("/")

    # Gateway architecture parameters fetch dynamically
    upi_target = payment_config["upi_id"]
    merchant_label = payment_config["merchant_name"]
    active_mode = payment_config["active_method"]
    price_target = product["price"]

    # Dynamic generation of deep linked UPI URI interface standard
    upi_raw_string = f"upi://pay?pa={upi_target}&pn={urllib.parse.quote(merchant_label)}&am={price_target}&tn=Order_Block_Ref_{product['id']}&cu=INR"
    
    # Render cloud service dynamic verification module via external QR compiler engine API
    compiled_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={urllib.parse.quote(upi_raw_string)}"
    if active_mode == "static_qr":
        compiled_qr_url = payment_config["static_qr_url"]

    content = f"""
    <div class="max-w-md mx-auto mt-2">
        <h1 class="text-xl font-black text-white mb-4 tracking-tight flex items-center gap-1.5"><i class="fas fa-shield-halved text-cyan-400"></i> SECURE ACCESS DISPATCH</h1>
        
        <div class="glass-card rounded-3xl p-5 border border-white/10 shadow-2xl relative overflow-hidden">
            <div class="flex items-center gap-3 mb-4 pb-4 border-b border-white/5">
                <img src="{product['image_url']}" class="w-16 h-16 object-cover rounded-xl border border-white/10" />
                <div>
                    <h3 class="font-extrabold text-white text-base leading-tight">{product['name']}</h3>
                    <p class="text-emerald-400 font-bold text-sm mt-0.5">₹{product['price']}</p>
                </div>
            </div>

            <div class="bg-black/30 border border-white/5 rounded-2xl p-4 text-center">
                <span class="text-[10px] font-black tracking-widest text-gray-500 uppercase block mb-3">SCAN METRIC SHIELD TO PAY</span>
                
                <div class="bg-white p-3 rounded-2xl inline-block shadow-xl transform transition hover:scale-102">
                    <img id="gateway-qr" src="{compiled_qr_url}" class="w-48 h-48 rounded-lg" alt="Secure Core Payment QR Router" />
                </div>
                
                <div class="text-gray-400 font-mono text-[10px] mt-3 tracking-tight break-all border-t border-white/5 pt-2">
                    Routing Mechanism: <span class="text-cyan-400 font-bold uppercase">{active_mode}</span>
                </div>
            </div>

            <div class="mt-4 space-y-2.5">
                <a href="{upi_raw_string}" class="block text-center bg-gradient-to-r from-emerald-400 to-cyan-400 hover:brightness-110 text-gray-950 font-black text-xs py-3.5 rounded-xl transition tracking-wider uppercase shadow-md">
                    LAUNCH MOBILE PAYMENT APP HUB
                </a>
                <button onclick="confirmSignal()" class="w-full text-center bg-white/5 hover:bg-white/10 text-gray-300 font-bold text-xs py-2.5 rounded-xl transition border border-white/5">
                    Verify Transaction Block Signal
                </button>
            </div>
        </div>
    </div>

    <script>
        function confirmSignal() {{
            alert("Signal Transmission Dispatched. Database ledger will update synchronization upon network settlement.");
            window.location.href = "/";
        }}
    </script>
    """
    return get_shared_layout(content, "home")


# ==========================================
# MODULE ROUTE 4: DYNAMIC GATEWAY ENGINE ENGINE MANAGMENT UI (`/pay`)
# ==========================================
@app.get("/pay", response_class=HTMLResponse)
def page_gateway_management():
    content = f"""
    <div class="mb-6 mt-1">
        <h1 class="text-2xl font-black text-amber-400 tracking-tight">GATEWAY CONTROL ARSENAL</h1>
        <p class="text-gray-400 text-xs">Configure parameters for routing merchant codes, UPI nodes, and static mapping buffers</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div class="glass-card rounded-2xl p-5 shadow-2xl lg:col-span-2">
            <h2 class="text-base font-extrabold text-white mb-4 flex items-center gap-1.5"><i class="fas fa-gear text-amber-400"></i> Mutate Terminal Configurations</h2>
            <form id="gateway-config-form" onsubmit="commitGateway(event)" class="space-y-4">
                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Active Routing Driver</label>
                    <select id="g-method" class="w-full bg-black/50 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-amber-400 text-xs font-bold transition">
                        <option value="upi_intent" {"selected" if payment_config["active_method"]=="upi_intent" else ""}>Dynamic UPI Routing Node (Recommended)</option>
                        <option value="phonepe_merchant" {"selected" if payment_config["active_method"]=="phonepe_merchant" else ""}>PhonePe Dedicated Merchant Matrix</option>
                        <option value="static_qr" {"selected" if payment_config["active_method"]=="static_qr" else ""}>Direct Static QR Code Vector Override</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Baseline Destination UPI Address</label>
                        <input type="text" id="g-upi" value="{payment_config['upi_id']}" class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2.5 text-white focus:outline-none focus:border-amber-400 text-xs font-mono"/>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Merchant Display Signature Name</label>
                        <input type="text" id="g-name" value="{payment_config['merchant_name']}" class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2.5 text-white focus:outline-none focus:border-amber-400 text-xs font-bold"/>
                    </div>
                </div>

                <div class="border-t border-white/5 pt-4">
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">PhonePe Core Merchant ID Token</label>
                    <input type="text" id="g-phonepe" value="{payment_config['phonepe_merchant_id']}" class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2.5 text-white focus:outline-none focus:border-amber-400 text-xs font-mono"/>
                </div>

                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Static Override QR CDN Target URL</label>
                    <input type="url" id="g-static-url" value="{payment_config['static_qr_url']}" class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2.5 text-white focus:outline-none focus:border-amber-400 text-xs"/>
                </div>

                <button type="submit" class="w-full bg-gradient-to-r from-amber-400 to-orange-500 hover:brightness-110 text-gray-950 font-black py-3 rounded-xl transition text-xs tracking-wider uppercase shadow-md">
                    COMMIT INTERFACE CONFIGURATION
                </button>
            </form>
        </div>

        <div class="glass-card rounded-2xl p-5 shadow-2xl space-y-4">
            <h2 class="text-base font-extrabold text-white flex items-center gap-1.5"><i class="fas fa-tower-broadcast text-cyan-400"></i> Signal Telemetry</h2>
            <div class="space-y-2 text-xs">
                <div class="bg-black/50 p-3 rounded-xl border border-white/5 flex justify-between items-center">
                    <span class="text-gray-500">Routing Module</span>
                    <span id="stat-method" class="text-cyan-400 font-mono font-bold uppercase">{payment_config['active_method']}</span>
                </div>
                <div class="bg-black/50 p-3 rounded-xl border border-white/5 flex justify-between items-center">
                    <span class="text-gray-500">Destination</span>
                    <span id="stat-upi" class="text-gray-300 font-mono">{payment_config['upi_id']}</span>
                </div>
            </div>
        </div>
    </div>

    <script>
        async function commitGateway(e) {{
            e.preventDefault();
            const payload = {{
                active_method: document.getElementById('g-method').value,
                upi_id: document.getElementById('g-upi').value,
                merchant_name: document.getElementById('g-name').value,
                phonepe_merchant_id: document.getElementById('g-phonepe').value,
                static_qr_url: document.getElementById('g-static-url').value
            }};

            const response = await fetch('/api/payment/config', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify(payload)
            }});

            if(response.ok) {{
                const data = await response.json();
                document.getElementById('stat-method').innerText = data.current.active_method;
                document.getElementById('stat-upi').innerText = data.current.upi_id;
                alert("Matrix Settings successfully saved.");
            }}
        }}
    </script>
    """
    return get_shared_layout(content, "pay")


# ==========================================
# MODULE ROUTE 5: MANAGEMENT CORE INVENTORY & CONFIG SITES
# ==========================================
@app.get("/admin", response_class=HTMLResponse)
def page_admin():
    content = """
    <div class="mb-6 mt-1">
        <h1 class="text-2xl font-black text-purple-400 tracking-tight">TERMINAL STOCK REGISTRY</h1>
        <p class="text-gray-400 text-xs">Inject new digital structural units into the live server cache loop</p>
    </div>
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div class="glass-card rounded-2xl p-5 shadow-2xl">
            <h2 class="text-base font-bold text-white mb-4"><i class="fas fa-plus text-purple-400"></i> Inject Block</h2>
            <form id="add-product-form" onsubmit="pushProduct(event)" class="space-y-3.5">
                <div>
                    <label class="block text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Product Title</label>
                    <input type="text" id="p-name" required class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-purple-400 text-xs font-semibold"/>
                </div>
                <div>
                    <label class="block text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Pricing Block (INR)</label>
                    <input type="number" step="0.01" id="p-price" required class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-purple-400 text-xs font-semibold"/>
                </div>
                <div>
                    <label class="block text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Image Address URL</label>
                    <input type="url" id="p-img" required class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-purple-400 text-xs"/>
                </div>
                <div>
                    <label class="block text-[9px] font-bold text-gray-400 uppercase tracking-wider mb-1">Summary Info</label>
                    <textarea id="p-desc" rows="3" required class="w-full bg-black/40 border border-white/10 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-purple-400 text-xs"></textarea>
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-purple-500 to-indigo-500 text-white font-black py-2.5 rounded-xl transition text-xs tracking-widest uppercase shadow-md">
                    EXECUTE FEED INJECTION
                </button>
            </form>
        </div>
        <div class="lg:col-span-2 glass-card rounded-2xl p-5 shadow-2xl">
            <h2 class="text-base font-bold text-white mb-4"><i class="fas fa-database text-purple-400"></i> Buffer Allocation Ledger</h2>
            <div id="admin-inventory-list" class="space-y-3 max-h-[55vh] overflow-y-auto pr-1"></div>
        </div>
    </div>

    <script>
        async function fetchAdminStock() {
            const res = await fetch('/api/products');
            const products = await res.json();
            const container = document.getElementById('admin-inventory-list');
            container.innerHTML = '';
            products.forEach(p => {
                container.innerHTML += `
                    <div class="flex items-center justify-between bg-black/30 border border-white/5 p-3 rounded-xl">
                        <div class="flex items-center gap-3">
                            <img src="${p.image_url}" class="w-10 h-10 rounded-lg object-cover bg-gray-900 border border-white/10" />
                            <div>
                                <h4 class="font-extrabold text-xs text-white">${p.name}</h4>
                                <p class="text-emerald-400 font-bold text-xs">₹${p.price}</p>
                            </div>
                        </div>
                        <button onclick="wipeStockItem(${p.id})" class="text-red-400 hover:text-white bg-red-500/10 hover:bg-red-500 px-3 py-1.5 rounded-xl text-[10px] font-bold transition">Wipe</button>
                    </div>
                `;
            });
        }

        async function pushProduct(e) {
            e.preventDefault();
            const payload = {
                name: document.getElementById('p-name').value,
                price: parseFloat(document.getElementById('p-price').value),
                image_url: document.getElementById('p-img').value,
                description: document.getElementById('p-desc').value
            };
            await fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });
            document.getElementById('add-product-form').reset();
            fetchAdminStock();
        }

        async function wipeStockItem(id) {
            if(confirm("Purge asset sequence?")) {
                await fetch('/api/products/' + id, { method: 'DELETE' });
                fetchAdminStock();
            }
        }
        window.onload = fetchAdminStock;
    </script>
    """
    return get_shared_layout(content, "admin")

@app.get("/settings", response_class=HTMLResponse)
def page_settings():
    content = """
    <div class="glass-card rounded-3xl p-6 shadow-2xl text-center max-w-xl mx-auto mt-6">
        <div class="bg-purple-500/10 border border-purple-500/20 p-4 rounded-2xl inline-block text-purple-400 text-2xl mb-4 shadow-inner">
            <i class="fas fa-book-bookmark"></i>
        </div>
        <h2 class="text-xl font-black text-white tracking-tight">OpenAPI Framework Matrix Swagger</h2>
        <p class="text-gray-400 text-xs mt-1.5 mb-5 leading-relaxed">Evaluate endpoint variables, data schemas, and trigger payloads seamlessly using the standard built-in Swagger engine core driver block configuration.</p>
        <a href="/docs" target="_blank" class="bg-gradient-to-r from-purple-500 via-indigo-500 to-cyan-500 text-white font-black text-xs tracking-widest px-6 py-3 rounded-xl transition shadow-lg uppercase">
            Initialize Core Docs UI <i class="fas fa-arrow-up-right-from-square text-[10px] ml-0.5"></i>
        </a>
    </div>
    """
    return get_shared_layout(content, "settings")
