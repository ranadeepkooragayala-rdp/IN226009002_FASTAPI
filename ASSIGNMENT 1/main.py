from fastapi import FastAPI , Query
 
app = FastAPI()
 
# ── Temporary data — acting as our database for now ──────────
products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 499,  'category': 'Electronics', 'in_stock': True },
    {'id': 2, 'name': 'Notebook',       'price':  99,  'category': 'Stationery',  'in_stock': True },
    {'id': 3, 'name': 'USB Hub',         'price': 799, 'category': 'Electronics', 'in_stock': False},
    {'id': 4, 'name': 'Pen Set',          'price':  49, 'category': 'Stationery',  'in_stock': True },
    {"id": 5, "name": "Laptop Stand", "price": 1299, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True}, 
    {"id": 7, "name": "Webcam", "price": 1899, "category": "Electronics", "in_stock": False},
    
]
 
# ── Endpoint  — Home ────────────────────────────────────────
@app.get('/')
def home():
    return {'message': 'Welcome to our E-commerce API'}
 
# ── Endpoint  — Return all products ──────────────────────────
@app.get('/products')
def get_all_products():
    return {'products': products, 'total': len(products)}
#--Endpoint -product filters--
@app.get('/products/filter')
def filter_products(
    category:  str  = Query(None, description='Electronics or Stationery'),
    max_price: int  = Query(None, description='Maximum price'),
    in_stock:  bool = Query(None, description='True = in stock only')
):
    result = products         
 
    if category:
        result = [p for p in result if p['category'] == category]
 
    if max_price:
        result = [p for p in result if p['price'] <= max_price]
 
    if in_stock is not None:
        result = [p for p in result if p['in_stock'] == in_stock]
 
    return {'filtered_products': result, 'count': len(result)}

# --Endpoint -- return deal products 
@app.get("/products/deals")
def get_product_deals():
    # This must be ABOVE the {product_id} route
    best_deal = min(products, key=lambda p: p["price"])
    premium_pick = max(products, key=lambda p: p["price"])
    return {
        "best_deal": best_deal, 
        "premium_pick": premium_pick
    }
 
# --Endpint  --return instock products--
@app.get("/products/instock")
def get_product_instock():
    available = [p for p in products if p.get("in_stock") is True]
    return {"in_stock_products": available, "count": len(available)}

# --Endpoint  --return product by category
@app.get("/products/category/{category_name}")
async def get_products_by_category(category_name: str):
    results = [p for p in products if p["category"].lower() == category_name.lower()]
    
    if not results:
        return {"error": "No products found in this category"}
        
    return results
# --Endpoint  --return product by id
@app.get("/products/{product_id}")
def get_product_by_id(product_id: int):
    # This acts as a 'catch-all' for any number entered after /products/
    product = next((p for p in products if p["id"] == product_id), None)
    return product or {"error": "Product not found"}

# -- Endpoint --return store summary
@app.get("/store/summary")
def get_store_summary():
    # 1. Calculate how many are in stock
    in_stock_count = len([p for p in products if p.get("in_stock") is True])
    
    # 2. Calculate how many are out of stock (Fixed line)
    out_stock_count = len(products) - in_stock_count
    
    # 3. Get the unique categories (Fixed line)
    categories = list(set(p["category"] for p in products))
    
    # 4. Return the summary
    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": in_stock_count,
        "out_of_stock": out_stock_count,
        "categories": categories
    }
# --Endpoint   --search product by name
@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    results = [
        p for p in products 
        if keyword.lower() in p["name"].lower()
    ]
    
    # 2. Check if the results list is empty
    if not results:
        return {"message": "No products matched your search"}
    
    # 3. Return the results along with the total count
    return {
        "results": results,
        "total_matches": len(results)
    }
