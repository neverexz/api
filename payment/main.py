from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

def load_config(filename):
    config = {}
    with open(filename, "r") as file:
        for line in file:
            key, value = line.strip().split("=", 1)
            config[key] = value
    return config

config = load_config("../codes.txt")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)
# better make another database
redis = get_redis_connection(
    host=config.get("host"),
    port=config.get("port"),
    password=config.get("password"),
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str # pending. completed, refunded

    class Meta:
        database = redis

@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)

@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks): # id, quantity
    body = await request.json()
    
    req = requests.get(f'http://localhost:8000/products/{body['id']}')
    product = req.json()
    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    
    background_tasks.add_task(order_completed, order)
    
    return order

def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
    
@app.get("/orders_all")    
def all():
    return [format(pk) for pk in Order.all_pks()]

def format(pk: str):
    order = Order.get(pk)
    
    return {
        'pk': order.pk,
        'product_id': order.product_id,
        'fee': order.fee,
        'total': order.total,
        'price': order.price,
        'quantity': order.quantity,
        'status': order.status
    }

@app.delete("/orders/{pk}")
def delete(pk: str):
    return Order.delete(pk)