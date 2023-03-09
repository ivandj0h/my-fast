from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from config import get_settings

# config
settings = get_settings()

# FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Redis
redis = get_redis_connection(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=settings.decode_responses,
)


# Redis Model
class Product(HashModel):
    name: str
    description: str
    price: float
    quantity: int

    class Meta:
        database = redis


# Routes
# Health Check
@app.get("/")
async def read_root():
    return {"Hello": "World"}


# Env Info
@app.get("/api/v1/envinfo")
async def read_envinfo():
    from config import get_settings
    settings = get_settings()
    return {
        "env_name": settings.env_name,
        "redis_host": settings.redis_host,
        "redis_port": settings.redis_port,
        "redis_password": settings.redis_password,
        "decode_responses": settings.decode_responses,
    }


# Product Format
def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
    }


# Get ALl Product Routes
@app.get("/api/v1/products")
async def get_all_products():
    return [format(pk) for pk in Product.all_pks()]


# Add Product Routes
@app.post("/api/v1/product")
async def create_product(product: Product):
    return product.save()


# Get Single Product Routes
@app.get("/api/v1/product/{pk}")
async def get_product(pk: str):
    return Product.get(pk)


# Update Product Routes
@app.put("/api/v1/product/{pk}")
async def update_product(pk: str, product: Product):
    return product.save()


# Delete Product Routes
@app.delete("/api/v1/product/{pk}")
async def delete_product(pk: str):
    return Product.delete(pk)
