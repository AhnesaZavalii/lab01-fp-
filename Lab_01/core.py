from typing import Callable, TypedDict

class Item(TypedDict):
    name: str
    price: float
    quantity: int
    category: str

class ItemWithTotal(Item):
    total: float

class CartResult(TypedDict):
    items: list[ItemWithTotal]
    subtotal: float
    total: float

DiscountFn = Callable[[Item, float], float]
CouponFn = Callable[[float], float]
TaxFn = Callable[[float], float]

def item_subtotal(item: Item) -> float:
    return item["price"] * item["quantity"]

def cart_subtotal(items: list[Item]) -> float:
    return sum(item_subtotal(item) for item in items)

def with_total(item: Item, total: float) -> ItemWithTotal:
    return {**item, "total": total}

def make_processor(
    category_discount: DiscountFn,
    coupon: CouponFn,
    tax: TaxFn,
) -> Callable[[list[Item]], CartResult]:

    def process(items: list[Item]) -> CartResult:
        new_items: list[ItemWithTotal] = []

        for item in items:
            subtotal = item_subtotal(item)
            discounted = category_discount(item, subtotal)
            after_coupon = coupon(discounted)
            total = tax(after_coupon)

            new_items.append(with_total(item, total))

        return {
            "items": new_items,
            "subtotal": cart_subtotal(items),
            "total": sum(item["total"] for item in new_items),
        }

    return process
