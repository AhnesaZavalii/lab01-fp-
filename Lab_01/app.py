from core import Item, make_processor

def category_discount(item: Item, subtotal: float) -> float:
    if item["category"] == "Books":
        return subtotal * 0.9

    return subtotal


def coupon(amount: float) -> float:
    return amount * 0.95


def tax(amount: float) -> float:
    return amount * 1.2


def run() -> None:
    items: list[Item] = [
        {
            "name": "Book",
            "price": 500.0,
            "quantity": 2,
            "category": "Books",
        },
        {
            "name": "T-shirt",
            "price": 900.0,
            "quantity": 1,
            "category": "Clothes",
        },
    ]

    process_cart = make_processor(
        category_discount,
        coupon,
        tax,
    )

    result = process_cart(items)

    print("Shopping cart:")

    for item in result["items"]:
        print(item)

    print("Subtotal:", result["subtotal"])
    print("Total with VAT:", round(result["total"], 2))


if __name__ == "__main__":
    run()


