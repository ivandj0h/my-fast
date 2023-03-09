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


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/envinfo")
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


@app.get("/products")
async def get_all_products():
    return Product.all_pks()


@app.post("/product")
async def create_product(product: Product):
    return product.save()