from datetime import datetime
from uuid import UUID # (universally unique identifier, UUID
from fastapi import status
from orders.app import app

order = {
    'id' : 'ff0f1355-e821-4178-9567-550dec27a373',
    'created': datetime.now()
}

@app.get('/orders')
def get_orders():
    return {'orders': [order]}

@app.post('/orders', status_code=status.HTTP_201_CREATED)
def create_order():
    return order

@app.get('/orders/{order_id}')
def get_order(order_id: UUID):
    return order

@app.put('/orders/{order_id}')
def update_order(order_id: UUID):
    return order

@app.delete('/orders/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: UUID):
    return {}

@app.post('/orders/{oder_id}/cancel')
def cancel_order():
    return order

@app.post('/orders/{oder_id}/pay')
def pay_order():
    return order