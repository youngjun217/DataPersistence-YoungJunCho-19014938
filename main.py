import sys
import os
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

from model.order import Order, OrderItem, OrderStatus
from repository.order_repository import OrderRepository


def demo_crud(repo: OrderRepository) -> None:
    print("=" * 50)
    print("  DataPersistence PoC - JSON CRUD 데모")
    print("=" * 50)

    # CREATE
    print("\n[CREATE] 주문 2건 생성")
    order1 = Order(
        id=str(uuid.uuid4())[:8],
        customer_name="홍길동",
        items=[
            OrderItem("노트북", 1, 1_500_000),
            OrderItem("마우스", 2, 35_000),
        ],
    )
    order2 = Order(
        id=str(uuid.uuid4())[:8],
        customer_name="김철수",
        items=[
            OrderItem("키보드", 1, 120_000),
        ],
    )
    repo.save(order1)
    repo.save(order2)
    print(f"  생성됨: {order1.id} ({order1.customer_name}), {order2.id} ({order2.customer_name})")

    # READ ALL
    print("\n[READ ALL] 전체 주문 목록")
    all_orders = repo.find_all()
    for o in all_orders:
        print(f"  - [{o.id}] {o.customer_name} | {o.status.value} | {o.total_price:,.0f}원")

    # READ ONE
    print(f"\n[READ ONE] ID={order1.id} 조회")
    found = repo.find_by_id(order1.id)
    if found:
        print(f"  -> {found.customer_name}, 총 {found.total_price:,.0f}원")

    # UPDATE
    print(f"\n[UPDATE] {order1.id} 상태를 PROCESSING으로 변경")
    updated = repo.update_status(order1.id, OrderStatus.PROCESSING)
    if updated:
        print(f"  -> 변경 후 상태: {updated.status.value}")

    # DELETE
    print(f"\n[DELETE] {order2.id} 삭제")
    deleted = repo.delete(order2.id)
    print(f"  -> 삭제 {'성공' if deleted else '실패'}")
    print(f"  -> 남은 주문 수: {repo.count()}건")

    print("\n[완료] orders.json 파일을 확인하세요.")
    print("=" * 50)


if __name__ == "__main__":
    repo = OrderRepository(db_path="data/orders.json")
    demo_crud(repo)
