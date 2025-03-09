from enum import Enum
from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, conlist, conint 

class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class StatusEnum(Enum):
    created = "created"
    paid = "paid"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"
    
class OrderItemSchema(BaseModel):
    product: str
    size: Size
    '''
    ge=1 → (greater or equal) значение должно быть ≥ 1
    le=100 → (less or equal) значение должно быть ≤ 100
    strict=True → запрещает неявное приведение типов (например, 1.5 вызовет ошибку)
    '''
    quantity: Optional[conint(ge=1, strict=True)] = 1

class CreateOrderSchema(BaseModel):
    order: conlist(OrderItemSchema, min_items=1)


class GetOrderSchema(CreateOrderSchema):
    id: UUID
    created: datetime
    status: StatusEnum


class GetOrdersSchema(BaseModel):
    orders: List[GetOrderSchema]