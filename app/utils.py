def product_helper(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "category": product["category"],
        "price": product["price"],
    }