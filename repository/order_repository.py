import json
import os
from typing import List, Optional

from model.order import Order, OrderStatus


class OrderRepository:
    def __init__(self, db_path: str = "data/orders.json"):
        self._db_path = db_path
        self._ensure_db()

    def _ensure_db(self) -> None:
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        if not os.path.exists(self._db_path):
            self._write([])

    def _read(self) -> List[dict]:
        with open(self._db_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, data: List[dict]) -> None:
        with open(self._db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # CREATE
    def save(self, order: Order) -> Order:
        records = self._read()
        records.append(order.to_dict())
        self._write(records)
        return order

    # READ ALL
    def find_all(self) -> List[Order]:
        return [Order.from_dict(r) for r in self._read()]

    # READ ONE
    def find_by_id(self, order_id: str) -> Optional[Order]:
        record = next((r for r in self._read() if r["id"] == order_id), None)
        return Order.from_dict(record) if record else None

    # UPDATE
    def update(self, order: Order) -> Optional[Order]:
        records = self._read()
        for i, r in enumerate(records):
            if r["id"] == order.id:
                records[i] = order.to_dict()
                self._write(records)
                return order
        return None

    def update_status(self, order_id: str, status: OrderStatus) -> Optional[Order]:
        order = self.find_by_id(order_id)
        if not order:
            return None
        order.status = status
        return self.update(order)

    # DELETE
    def delete(self, order_id: str) -> bool:
        records = self._read()
        filtered = [r for r in records if r["id"] != order_id]
        if len(filtered) == len(records):
            return False
        self._write(filtered)
        return True

    def count(self) -> int:
        return len(self._read())
