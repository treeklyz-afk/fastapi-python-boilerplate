from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="⚡ CyberShop 3D Engine",
    description="Next-Gen 3D/iOS Vibe Gaming E-Commerce Storefront",
    version="2.0.0"
)

# --- IN-MEMORY DATABASE ---
products_db = [
    {
        "id": 1,
        "name": "Wireless AirBuds Pro",
        "price": 2999.0,
        "description": "Active noise cancellation with extra deep holographic bass and 30hrs runtime.",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"
    },
    {
        "id": 2,
        "name": "AMOLED Cyber Watch",
        "price": 4499.0,
        "description": "Always-on quantum sync layer, biometric radar tracker, and tactile metallic chassis.",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&q=80"
    },
    {
        "id": 3,
        "name": "Stealth Leather Armor Wallet",
        "price": 999.0,
        "description": "Aerospace grade RFID defense nodes bound inside premium full-grain leather geometry.",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&q=80"
    }
]

class ProductModel(BaseModel):
    name: str
    price: float
    description: str
    image_url: str

# ==========================================
# REST API ENDPOINTS
# ==========================================
@app.get("/api/products", response_model=List[dict])
def get_all_products():
    return products_db

@app.post("/api/products")
def add_new_product(product: ProductModel):
    new_id = max([p["id"] for p in products_db], default=0) + 1
    product_dict = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image_url": product.image_url or "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&q=80"
    }
    products_db.append(product_dict)
    return {"status": "success", "product": product_dict}

@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    global products_db
    initial_length = len(products_db)
    products_db = [p for p in products_db if p["id"] != product_id]
    if len(products_db) < initial_length:
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Not found")


# ==========================================
# UI LAYOUT ENGINE (iOS + 3D Gaming Vibe)
# ==========================================
def get_shared_layout(content: str, active_tab: str) -> str:
    # Python formatting conflicts handle karne ke liye double curly braces {{}} use kiye hain CSS/JS me
    return f"""
    <!DOCTYPE html>
    <html lang="en" class="scroll-smooth">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
        <title>⚡ CyberShop 3D</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Plus Jakarta Sans', sans-serif;
                background: radial-gradient(circle at 50% 0%, #1a102f 0%, #0b0713 70%, #020105 100%);
                -webkit-font-smoothing: antialiased;
            }}
            .glass-card {{
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                box-shadow: inset 0 1px 1px rgba(255, 255, 255, 0.1), 0 20px 40px rgba(0, 0, 0, 0.3);
            }}
            .gaming-glow:hover {{
                box-shadow: 0 0 30px rgba(0, 255, 170, 0.25);
                border-color: rgba(0, 255, 170, 0.4);
                transform: translateY(-6px) scale(1.02);
            }}
            .ios-blur-nav {{
                background: rgba(11, 7, 19, 0.6);
                backdrop-filter: blur(30px);
                -webkit-backdrop-filter: blur(30px);
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }}
            ::-webkit-scrollbar {{
                width: 6px;
            }}
            ::-webkit-scrollbar-track {{
                background: #020105;
            }}
            ::-webkit-scrollbar-thumb {{
                background: #3b2073;
                border-radius: 10px;
            }}
        </style>
    </head>
    <body class="text-gray-100 min-h-screen flex flex-col pb-28 md:pb-0">
        
        <nav class="ios-blur-nav sticky top-0 z-50 px-6 py-4 shadow-2xl">
            <div class="max-w-5xl mx-auto flex justify-between items-center">
                <a href="/" class="text-2xl font-extrabold tracking-tight bg-gradient-to-r from-cyan-400 via-emerald-400 to-indigo-500 bg-clip-text text-transparent flex items-center gap-2">
                    <i class="fas fa-cube animate-spin [animation-duration:6s]"></i> CYBER✕SHOP
                </a>
                <div class="hidden md:flex bg-white/5 border border-white/10 px-2 py-1 rounded-full space-x-1">
                    <a href="/" class="px-5 py-1.5 rounded-full text-sm font-semibold transition {"bg-gradient-to-r from-emerald-500 to-cyan-500 text-gray-950 shadow-lg" if active_tab == 'home' else "text-gray-400 hover:text-white"}" >Store</a>
                    <a href="/admin" class="px-5 py-1.5 rounded-full text-sm font-semibold transition {"bg-gradient-to-r from-emerald-500 to-cyan-500 text-gray-950 shadow-lg" if active_tab == 'admin' else "text-gray-400 hover:text-white"}" >Admin Panel</a>
                    <a href="/settings" class="px-5 py-1.5 rounded-full text-sm font-semibold transition {"bg-gradient-to-r from-emerald-500 to-cyan-500 text-gray-950 shadow-lg" if active_tab == 'settings' else "text-gray-400 hover:text-white"}" >Settings</a>
                </div>
            </div>
        </nav>

        <main class="flex-1 max-w-5xl w-full mx-auto p-5 mt-2">
            {content}
        </main>

        <div class="md:hidden fixed bottom-6 left-4 right-4 bg-black/60 backdrop-blur-3xl border border-white/10 shadow-[0_25px_50px_-12px_rgba(0,0,0,0.7)] rounded-3xl flex justify-around py-3.5 z-50 px-4">
            <a href="/" class="flex flex-col items-center transition-all duration-200 active:scale-90 {"text-emerald-400" if active_tab == 'home' else "text-gray-400 hover:text-white"}">
                <i class="fas fa-layer-group text-xl"></i>
                <span class="text-[10px] font-bold mt-1 tracking-wide uppercase">Discover</span>
            </a>
            <a href="/admin" class="flex flex-col items-center transition-all duration-200 active:scale-90 {"text-emerald-400" if active_tab == 'admin' else "text-gray-400 hover:text-white"}">
                <i class="fas fa-shield-halved text-xl"></i>
                <span class="text-[10px] font-bold mt-1 tracking-wide uppercase">Terminal</span>
            </a>
            <a href="/settings" class="flex flex-col items-center transition-all duration-200 active:scale-90 {"text-emerald-400" if active_tab == 'settings' else "text-gray-400 hover:text-white"}">
                <i class="fas fa-sliders text-xl"></i>
                <span class="text-[10px] font-bold mt-1 tracking-wide uppercase">Config</span>
            </a>
        </div>

    </body>
    </html>
    """

# 1. Storefront Home Page
@app.get("/", response_class=HTMLResponse)
def storefront_index():
    content = """
    <div class="mb-8 mt-2 flex justify-between items-end">
        <div>
            <h1 class="text-3xl font-extrabold tracking-tight text-white flex items-center gap-2">Trending Drops <span class="animate-pulse text-red-500 text-2xl">⚡</span></h1>
            <p class="text-gray-400 text-xs mt-1">Premium 3D hyper-tuned assets ready for deployment</p>
        </div>
        <div class="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-xs text-emerald-400 font-bold tracking-widest uppercase">Live Nodes</div>
    </div>

    <div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
        </div>

    <script>
        async function loadProducts() {
            const res = await fetch('/api/products');
            const products = await res.json();
            const grid = document.getElementById('product-grid');
            grid.innerHTML = '';
            
            if(products.length === 0) {
                grid.innerHTML = `<div class="col-span-full text-center py-20 glass-card rounded-2xl text-gray-500 font-medium">Vault Empty. Open Terminal Node to push cargo.</div>`;
                return;
            }

            products.forEach(p => {
                grid.innerHTML += `
                    <div class="glass-card gaming-glow rounded-3xl overflow-hidden transition-all duration-300 ease-out flex flex-col group">
                        <div class="relative overflow-hidden aspect-[4/3] bg-gray-950">
                            <div class="absolute inset-0 bg-gradient-to-t from-gray-950 via-transparent to-transparent z-10"></div>
                            <img src="${p.image_url}" class="w-full h-full object-cover transform group-hover:scale-110 transition duration-700 ease-out filter brightness-90 group-hover:brightness-100" alt="${p.name}"/>
                            <span class="absolute top-4 right-4 bg-black/70 backdrop-blur-md text-cyan-400 border border-cyan-400/30 font-mono text-xs px-2.5 py-1 rounded-full font-bold z-20">ID-0${p.id}</span>
                        </div>
                        <div class="p-5 flex flex-col flex-1 justify-between relative z-20 bg-gray-950/40">
                            <div>
                                <h3 class="font-extrabold text-xl text-white tracking-tight mb-2 group-hover:text-emerald-400 transition">${p.name}</h3>
                                <p class="text-gray-400 text-xs leading-relaxed line-clamp-2">${p.description}</p>
                            </div>
                            <div class="flex justify-between items-center mt-6 pt-4 border-t border-white/5">
                                <div class="flex flex-col">
                                    <span class="text-[9px] text-gray-500 font-bold uppercase tracking-wider">Value Core</span>
                                    <span class="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">₹${p.price}</span>
                                </div>
                                <button onclick="alert('Transaction Authorized! Value: ₹${p.price}')" class="bg-gradient-to-r from-emerald-400 to-cyan-400 hover:from-emerald-500 hover:to-cyan-500 text-gray-950 font-extrabold text-xs px-5 py-3 rounded-xl transition shadow-[0_10px_20px_rgba(0,255,170,0.2)] hover:shadow-[0_10px_25px_rgba(0,255,170,0.4)] active:scale-95 transform">
                                    ACQUIRE DECK
                                </button>
                            </div>
                        </div>
                    </div>
                `;
            });
        }
        window.onload = loadProducts;
    </script>
    """
    return get_shared_layout(content, "home")


# 2. Admin Inventory Panel
@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    content = """
    <div class="mb-8 mt-2">
        <h1 class="text-3xl font-extrabold tracking-tight text-amber-400 flex items-center gap-2">🛡️ Terminal Access Node</h1>
        <p class="text-gray-400 text-xs mt-1">Directly control active data blocks and matrix inventories</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div class="glass-card rounded-3xl p-6 shadow-2xl relative overflow-hidden">
            <div class="absolute -top-12 -right-12 w-24 h-24 bg-emerald-500/10 rounded-full blur-2xl"></div>
            <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2"><i class="fas fa-square-plus text-emerald-400"></i> Inject Asset</h2>
            <form id="add-product-form" onsubmit="submitForm(event)" class="space-y-4">
                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Asset Label</label>
                    <input type="text" id="p-name" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-400 text-sm font-medium transition"/>
                </div>
                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Price Target (INR)</label>
                    <input type="number" step="0.01" id="p-price" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-400 text-sm font-medium transition"/>
                </div>
                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Media Source URL</label>
                    <input type="url" id="p-img" placeholder="https://..." class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-400 text-sm font-medium transition"/>
                </div>
                <div>
                    <label class="block text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-1.5">Core Specifications</label>
                    <textarea id="p-desc" rows="3" required class="w-full bg-black/40 border border-white/10 rounded-xl px-4 py-2.5 text-white focus:outline-none focus:border-emerald-400 text-sm font-medium transition"></textarea>
                </div>
                <button type="submit" class="w-full bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-500 hover:to-orange-600 text-gray-950 font-extrabold py-3 rounded-xl transition text-xs tracking-wider uppercase shadow-lg active:scale-95 transform mt-2">
                    Execute Matrix Feed
                </button>
            </form>
        </div>

        <div class="lg:col-span-2 glass-card rounded-3xl p-6 shadow-2xl">
            <h2 class="text-lg font-bold text-white mb-5 flex items-center gap-2"><i class="fas fa-network-wired text-cyan-400"></i> Operational Modules</h2>
            <div id="admin-product-list" class="space-y-4 max-h-[60vh] overflow-y-auto pr-2">
                </div>
        </div>
    </div>

    <script>
        async function fetchAdminInventory() {
            const res = await fetch('/api/products');
            const products = await res.json();
            const listDiv = document.getElementById('admin-product-list');
            listDiv.innerHTML = '';

            if(products.length === 0) {
                listDiv.innerHTML = '<p class="text-center text-gray-500 py-10 font-mono text-xs">No assets linked inside registry.</p>';
                return;
            }

            products.forEach(p => {
                listDiv.innerHTML += `
                    <div class="flex items-center gap-4 bg-black/30 border border-white/5 p-4 rounded-2xl justify-between hover:border-white/10 transition group">
                        <div class="flex items-center gap-4">
                            <img src="${p.image_url}" class="w-14 h-14 rounded-xl object-cover bg-gray-900 border border-white/10 shadow-inner group-hover:scale-105 transition" />
                            <div>
                                <h4 class="font-bold text-sm text-white tracking-tight">${p.name}</h4>
                                <p class="text-emerald-400 font-black text-xs mt-0.5">₹${p.price}</p>
                            </div>
                        </div>
                        <button onclick="deleteProductItem(${p.id})" class="text-red-400 hover:text-white bg-red-500/10 hover:bg-red-500 border border-red-500/20 px-4 py-2 rounded-xl text-xs font-bold transition-all transform active:scale-90 flex items-center gap-1.5">
                            <i class="fas fa-bolt-lightning text-[10px]"></i> Wipe
                        </button>
                    </div>
                `;
            });
        }

        async function submitForm(e) {
            e.preventDefault();
            const payload = {
                name: document.getElementById('p-name').value,
                price: parseFloat(document.getElementById('p-price').value),
                image_url: document.getElementById('p-img').value,
                description: document.getElementById('p-desc').value
            };

            const response = await fetch('/api/products', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(payload)
            });

            if(response.ok) {
                document.getElementById('add-product-form').reset();
                fetchAdminInventory();
            }
        }

        async function deleteProductItem(id) {
            if(confirm("Confirm deletion of structural element ID-0" + id + "?")) {
                await fetch('/api/products/' + id, { method: 'DELETE' });
                fetchAdminInventory();
            }
        }

        window.onload = fetchAdminInventory;
    </script>
    """
    return get_shared_layout(content, "admin")


# 3. Settings Configuration Panel
@app.get("/settings", response_class=HTMLResponse)
def settings_panel():
    content = """
    <div class="mb-8 mt-2">
        <h1 class="text-3xl font-extrabold tracking-tight text-purple-400 flex items-center gap-2">⚙️ Operational Config</h1>
        <p class="text-gray-400 text-xs mt-1">Modify terminal diagnostics, schemas, and live compiler vectors</p>
    </div>

    <div class="max-w-2xl mx-auto space-y-6">
        <div class="glass-card rounded-3xl p-6 shadow-2xl relative overflow-hidden group hover:border-purple-500/40 transition duration-300">
            <div class="absolute -top-16 -right-16 w-32 h-32 bg-purple-500/10 rounded-full blur-3xl group-hover:bg-purple-500/20 transition"></div>
            <div class="flex items-start gap-5">
                <div class="bg-gradient-to-br from-purple-500 to-indigo-600 p-3.5 rounded-2xl text-white text-xl shadow-lg">
                    <i class="fas fa-terminal"></i>
                </div>
                <div class="flex-1">
                    <h3 class="font-extrabold text-white text-base tracking-tight">Swagger Open-API Compiler</h3>
                    <p class="text-gray-400 text-xs mt-1 mb-5 leading-relaxed">
                        Access real-time documentation mapping data streams directly into external Android telemetry engines or external endpoints.
                    </p>
                    <a href="/docs" target="_blank" class="inline-flex items-center gap-2 bg-gradient-to-r from-purple-500 to-indigo-500 hover:from-purple-600 hover:to-indigo-600 text-white font-extrabold px-5 py-3 rounded-xl text-xs tracking-wider uppercase transition shadow-md active:scale-95 transform">
                        LAUNCH COMPILED DOCS <i class="fas fa-arrow-up-right-from-square text-[10px]"></i>
                    </a>
                </div>
            </div>
        </div>

        <div class="glass-card rounded-3xl p-6 shadow-2xl">
            <h3 class="font-bold text-white text-sm tracking-widest uppercase mb-4 flex items-center gap-2 text-cyan-400"><i class="fas fa-circle-info"></i> System Blueprint Data</h3>
            <div class="grid grid-cols-2 gap-4 text-xs font-medium">
                <div class="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span class="text-gray-500 block text-[9px] uppercase font-bold tracking-wider">Framework Driver</span>
                    <span class="text-gray-200 mt-1 block font-mono">FastAPI ASGI v0.135+</span>
                </div>
                <div class="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span class="text-gray-500 block text-[9px] uppercase font-bold tracking-wider">Cache Layer</span>
                    <span class="text-gray-200 mt-1 block font-mono">In-Memory RAM Array</span>
                </div>
                <div class="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span class="text-gray-500 block text-[9px] uppercase font-bold tracking-wider">Interface Core</span>
                    <span class="text-gray-200 mt-1 block font-mono">Tailwind Glass JIT</span>
                </div>
                <div class="bg-black/40 p-4 rounded-xl border border-white/5">
                    <span class="text-gray-500 block text-[9px] uppercase font-bold tracking-wider">Deployment Engine</span>
                    <span class="text-emerald-400 font-bold mt-1 block font-mono">Vercel Hyper Edge</span>
                </div>
            </div>
        </div>
    </div>
    """
    return get_shared_layout(content, "settings")
