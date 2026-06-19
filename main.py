from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="⚡ Mobile Shop Engine",
    description="Complete E-Commerce API with integrated Storefront and Admin dashboard",
    version="1.0.0"
)

# --- IN-MEMORY DATABASE (Initial Sample Products) ---
products_db = [
    {
        "id": 1,
        "name": "Wireless AirBuds Pro",
        "price": 2999.0,
        "description": "Active noise cancellation with extra deep bass and 30hrs battery life.",
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500&q=80"
    },
    {
        "id": 2,
        "name": "AMOLED Smart Watch",
        "price": 4499.0,
        "description": "Always-on display, heart rate monitor, fitness tracking, and metallic build.",
        "image_url": "https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=500&q=80"
    },
    {
        "id": 3,
        "name": "Premium Leather Wallet",
        "price": 999.0,
        "description": "Genuine leather minimalist wallet featuring high-grade RFID blocking technology.",
        "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500&q=80"
    }
]

# --- PYDANTIC MODEL ---
class ProductModel(BaseModel):
    name: str
    price: float
    description: str
    image_url: str


# ==========================================
# PART 1: CORE REST API ENDPOINTS
# ==========================================

@app.get("/api/products", response_model=List[dict], tags=["Products API"])
def get_all_products():
    """Saare products list karne ke liye API"""
    return products_db

@app.post("/api/products", tags=["Products API"])
def add_new_product(product: ProductModel):
    """Admin panel se naya product add karne ke liye API"""
    new_id = max([p["id"] for p in products_db], default=0) + 1
    product_dict = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "image_url": product.image_url or "https://images.unsplash.com/photo-1531403009284-440f080d1e12?w=500&q=80"
    }
    products_db.append(product_dict)
    return {"status": "success", "message": "Product added successfully!", "product": product_dict}

@app.delete("/api/products/{product_id}", tags=["Products API"])
def delete_product(product_id: int):
    """Admin panel se kisi product ko delete karne ki API"""
    global products_db
    initial_length = len(products_db)
    products_db = [p for p in products_db if p["id"] != product_id]
    
    if len(products_db) < initial_length:
        return {"status": "success", "message": f"Product {product_id} deleted successfully."}
    raise HTTPException(status_code=404, detail="Product not found.")


# ==========================================
# PART 2: MOBILE-FRIENDLY FRONTEND RE-RENDERERS
# ==========================================

# Common Tailwind + Flow Style Wrapper Header/Navbar
def get_shared_layout(content: str, active_tab: str) -> str:
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>⚡ QuickShop Mobile Hub</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-weight/6.4.0/css/all.min.css">
    </head>
    <body class="bg-gray-900 text-gray-100 min-h-screen flex flex-col pb-20 md:pb-0">
        
        <nav class="bg-gray-800 border-b border-gray-700 sticky top-0 z-50 px-4 py-3 shadow-md">
            <div class="max-w-6xl mx-auto flex justify-between items-center">
                <a href="/" class="text-xl font-bold tracking-wider text-emerald-400 flex items-center gap-2">
                    <i class="fas fa-bolt"></i> QuickShop
                </a>
                <div class="hidden md:flex space-x-6">
                    <a href="/" class="{"text-emerald-400 font-semibold" if active_tab == 'home' else "text-gray-400 hover:text-white"} transition">Store</a>
                    <a href="/admin" class="{"text-emerald-400 font-semibold" if active_tab == 'admin' else "text-gray-400 hover:text-white"} transition">Admin Panel</a>
                    <a href="/settings" class="{"text-emerald-400 font-semibold" if active_tab == 'settings' else "text-gray-400 hover:text-white"} transition">Settings</a>
                </div>
            </div>
        </nav>

        <main class="flex-1 max-w-6xl w-full mx-auto p-4">
            {content}
        </main>

        <div class="md:hidden fixed bottom-0 left-0 right-0 bg-gray-800 border-t border-gray-700 shadow-xl flex justify-around py-2 z-50">
            <a href="/" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'home' else "text-gray-400"}">
                <i class="fas fa-store text-lg"></i>
                <span class="text-xs mt-1">Shop</span>
            </a>
            <a href="/admin" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'admin' else "text-gray-400"}">
                <i class="fas fa-user-shield text-lg"></i>
                <span class="text-xs mt-1">Admin</span>
            </a>
            <a href="/settings" class="flex flex-col items-center {"text-emerald-400" if active_tab == 'settings' else "text-gray-400"}">
                <i class="fas fa-cog text-lg"></i>
                <span class="text-xs mt-1">Settings</span>
            </a>
        </div>

    </body>
    </html>
    """

# 1. Storefront Home Route
@app.get("/", response_class=HTMLResponse)
def storefront_index():
    content = """
    <div class="mb-6 mt-2">
        <h1 class="text-2xl font-bold">Trending Products 🔥</h1>
        <p class="text-gray-400 text-sm">Handpicked premium collection just for you</p>
    </div>

    <div id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        </div>

    <script>
        async function loadProducts() {
            const res = await fetch('/api/products');
            const products = await res.json();
            const grid = document.getElementById('product-grid');
            grid.innerHTML = '';
            
            if(products.length === 0) {
                grid.innerHTML = `<div class="col-span-full text-center py-12 text-gray-500">No products found in store inventory.</div>`;
                return;
            }

            products.forEach(p => {
                grid.innerHTML += `
                    <div class="bg-gray-800 border border-gray-700 rounded-xl overflow-hidden shadow-lg hover:border-gray-600 transition flex flex-col">
                        <img src="${p.image_url}" class="w-full h-48 object-cover bg-gray-700" alt="${p.name}"/>
                        <div class="p-4 flex flex-col flex-1 justify-between">
                            <div>
                                <h3 class="font-bold text-lg text-white mb-1">${p.name}</h3>
                                <p class="text-gray-400 text-xs line-clamp-2 mb-3">${p.description}</p>
                            </div>
                            <div class="flex justify-between items-center mt-4">
                                <span class="text-xl font-extrabold text-emerald-400">₹${p.price}</span>
                                <button onclick="alert('Order Feature coming soon! Total: ₹${p.price}')" class="bg-emerald-500 hover:bg-emerald-600 text-gray-900 font-bold text-sm px-4 py-2 rounded-lg transition shadow-md">
                                    Buy Now
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


# 2. Admin Inventory Dashboard Route
@app.get("/admin", response_class=HTMLResponse)
def admin_panel():
    content = """
    <div class="mb-6 mt-2">
        <h1 class="text-2xl font-bold text-amber-400">🛡️ Store Control Center</h1>
        <p class="text-gray-400 text-sm">Add or eliminate items from live active retail inventory</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        <div class="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-xl">
            <h2 class="text-lg font-bold text-white mb-4"><i class="fas fa-plus-circle text-emerald-400 mr-1"></i> Add New Product</h2>
            <form id="add-product-form" onsubmit="submitForm(event)" class="space-y-4">
                <div>
                    <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Product Title</label>
                    <input type="text" id="p-name" required class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-sm"/>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Price (INR)</label>
                    <input type="number" step="0.01" id="p-price" required class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-sm"/>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Image CDN Address / URL</label>
                    <input type="url" id="p-img" placeholder="https://unsplash.com/..." class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-sm"/>
                </div>
                <div>
                    <label class="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-1">Product Summary</label>
                    <textarea id="p-desc" rows="3" required class="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500 text-sm"></textarea>
                </div>
                <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-600 text-gray-900 font-bold py-2 rounded-lg transition text-sm shadow-md">
                    Publish Product Live
                </button>
            </form>
        </div>

        <div class="lg:col-span-2 bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-xl">
            <h2 class="text-lg font-bold text-white mb-4"><i class="fas fa-boxes text-amber-400 mr-1"></i> Current Catalog Stock</h2>
            <div id="admin-product-list" class="space-y-3 max-h-[60vh] overflow-y-auto pr-1">
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
                listDiv.innerHTML = '<p class="text-center text-gray-500 py-6">No items listed in database inventory.</p>';
                return;
            }

            products.forEach(p => {
                listDiv.innerHTML += `
                    <div class="flex items-center gap-3 bg-gray-900 border border-gray-700 p-3 rounded-xl justify-between">
                        <div class="flex items-center gap-3">
                            <img src="${p.image_url}" class="w-12 h-12 rounded-lg object-cover bg-gray-800" />
                            <div>
                                <h4 class="font-bold text-sm text-white">${p.name}</h4>
                                <p class="text-emerald-400 font-semibold text-xs">₹${p.price}</p>
                            </div>
                        </div>
                        <button onclick="deleteProductItem(${p.id})" class="text-red-400 hover:text-red-500 bg-red-500/10 hover:bg-red-500/20 px-3 py-1.5 rounded-lg text-xs font-semibold transition">
                            <i class="fas fa-trash"></i> Remove
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
            if(confirm("Confirm removal of this inventory item?")) {
                await fetch('/api/products/' + id, { method: 'DELETE' });
                fetchAdminInventory();
            }
        }

        window.onload = fetchAdminInventory;
    </script>
    """
    return get_shared_layout(content, "admin")


# 3. Settings Dashboard Route (Linking to API documentation)
@app.get("/settings", response_class=HTMLResponse)
def settings_panel():
    content = """
    <div class="mb-6 mt-2">
        <h1 class="text-2xl font-bold text-gray-100">⚙️ System Configuration</h1>
        <p class="text-gray-400 text-sm">Manage API connections, documentation, and app specifications</p>
    </div>

    <div class="max-w-2xl mx-auto space-y-4">
        <div class="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-lg">
            <div class="flex items-start gap-4">
                <div class="bg-emerald-500/10 p-3 rounded-xl text-emerald-400 text-xl">
                    <i class="fas fa-book"></i>
                </div>
                <div class="flex-1">
                    <h3 class="font-bold text-white text-base">Interactive Swagger Core Engine</h3>
                    <p class="text-gray-400 text-xs mt-1 mb-4 leading-relaxed">
                        Open up-to-date OpenAPI developer integration docs to build or test android application connectivity logic endpoints seamlessly.
                    </p>
                    <a href="/docs" target="_blank" class="inline-flex items-center gap-2 bg-emerald-500 hover:bg-emerald-600 text-gray-900 font-bold px-4 py-2 rounded-lg text-xs transition shadow-md">
                        Explore Swagger UI <i class="fas fa-external-link-alt text-[10px]"></i>
                    </a>
                </div>
            </div>
        </div>

        <div class="bg-gray-800 border border-gray-700 rounded-xl p-5 shadow-lg">
            <h3 class="font-bold text-white text-base mb-3"><i class="fas fa-info-circle text-blue-400 mr-1"></i> Technical Diagnostics</h3>
            <div class="grid grid-cols-2 gap-3 text-xs">
                <div class="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">
                    <span class="text-gray-500 block">Framework Baseline</span>
                    <span class="text-gray-200 font-semibold mt-1 block">FastAPI ASGI</span>
                </div>
                <div class="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">
                    <span class="text-gray-500 block">Database Layer</span>
                    <span class="text-gray-200 font-semibold mt-1 block">In-Memory Store</span>
                </div>
                <div class="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">
                    <span class="text-gray-500 block">Responsive Pipeline</span>
                    <span class="text-gray-200 font-semibold mt-1 block">Tailwind CDN Core</span>
                </div>
                <div class="bg-gray-900/50 p-3 rounded-lg border border-gray-700/50">
                    <span class="text-gray-500 block">Runtime Target</span>
                    <span class="text-emerald-400 font-bold mt-1 block">Vercel Compliant</span>
                </div>
            </div>
        </div>
    </div>
    """
    return get_shared_layout(content, "settings")
