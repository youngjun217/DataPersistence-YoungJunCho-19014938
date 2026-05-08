from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class OrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class OrderItem:
    product_name: str
    quantity: int
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price

    def to_dict(self) -> dict:
        return {
            "product_name": self.product_name,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "OrderItem":
        return cls(
            product_name=data["product_name"],
            quantity=data["quantity"],
            unit_price=data["unit_price"],
        )


@dataclass
class Order:
    id: str
    customer_name: str
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def total_price(self) -> float:
        return sum(item.subtotal for item in self.items)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "items": [item.to_dict() for item in self.items],
            "status": self.status.value,
            "created_at": self.created_at,
            "total_price": self.total_price,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        return cls(
            id=data["id"],
            customer_name=data["customer_name"],
            items=[OrderItem.from_dict(i) for i in data.get("items", [])],
            status=OrderStatus(data.get("status", "pending")),
            created_at=data.get("created_at", datetime.now().isoformat()),
        )
