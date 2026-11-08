from copy import deepcopy

from core import (
    Item,
    item_subtotal,
    cart_subtotal,
    make_processor,
)

def test_item_subtotal() -> None:
    item: Item = {
        "name": "Book",
        "price": 500.0,
        "quantity": 2,
        "category": "Books",
    }

    assert item_subtotal(item) == 1000.0

def test_cart_subtotal() -> None:
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
    assert cart_subtotal(items) == 1900.0

def test_input_is_not_modified() -> None:
    items: list[Item] = [
        {
            "name": "Book",
            "price": 500.0,
            "quantity": 2,
            "category": "Books",
        }
    ]
    original = deepcopy(items)

    processor = make_processor(
        lambda item, amount: amount * 0.9,
        lambda amount: amount * 0.95,
        lambda amount: amount * 1.2,
    )
    processor(items)
    assert items == original

def test_referential_transparency() -> None:
    item: Item = {
        "name": "Book",
        "price": 500.0,
        "quantity": 2,
        "category": "Books",
    }

    assert item_subtotal(item) == item_subtotal(item)

def test_processor_uses_policies() -> None:
    items: list[Item] = [
        {
            "name": "Book",
            "price": 400.0,
            "quantity": 1,
            "category": "Books",
        }
    ]
    processor = make_processor(
        lambda item, amount: amount - 10,
        lambda amount: amount - 5,
        lambda amount: amount * 1.2,
    )
    result = processor(items)
    assert result["items"][0]["total"] == 462.0

def test_empty_cart() -> None:
    processor = make_processor(
        lambda item, amount: amount,
        lambda amount: amount,
        lambda amount: amount * 1.2,
    )
    result = processor([])
    assert result["items"] == []
    assert result["subtotal"] == 0
    assert result["total"] == 0