def cart_item_count(request):
    cart = request.session.get('cart', {})

    count = 0

    for cart_item in cart.values():
        if isinstance(cart_item, dict):
            count += cart_item.get('quantity', 0)
        else:
            # Purane cart data ke liye backward compatibility
            count += cart_item

    return {
        'cart_item_count': count
    }
