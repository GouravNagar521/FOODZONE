from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import (
    FoodItem,
    FoodCustomization,
    Order,
    OrderItem,
    ContactMessage,
    TableBooking
)
from django.db import transaction
from django.http import JsonResponse
def Homeview(request):
    food_items = FoodItem.objects.all()[:4]

    return render(request, 'home.html', {
        'food_items': food_items
    })


def Aboutview(request):
    return render(request, 'about.html')


def Menuview(request):
    food_items = FoodItem.objects.prefetch_related('customization_options').all()

    for item in food_items:
        options = item.customization_options.filter(
            is_active=True
        ).order_by('group_name', 'id')

        groups = {}

        for option in options:
            if option.group_name not in groups:
                groups[option.group_name] = {
                    'name': option.group_name,
                    'type': option.selection_type,
                    'required': option.is_required,
                    'options': []
                }

            groups[option.group_name]['options'].append(option)

        item.customization_groups = list(groups.values())

    return render(request, 'menu.html', {'food_items': food_items})
from datetime import date as date_type, time as time_type

def Booktableview(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        guests = request.POST.get('guests')
        date_value = request.POST.get('date')
        time_value = request.POST.get('time')
        special_request = request.POST.get('request', '').strip()

        if not all([name, email, phone, guests, date_value, time_value]):
            return render(request, 'book_table.html', {
                'error': 'Please fill all required fields.'
            })

        if not phone.isdigit() or len(phone) != 10:
            return render(request, 'book_table.html', {
                'error': 'Enter a valid 10-digit phone number.'
            })

        try:
            booking_date = date_type.fromisoformat(date_value)
            booking_time = time_type.fromisoformat(time_value)
            guest_count = int(guests)

            if guest_count < 1 or guest_count > 8:
                raise ValueError

            if booking_date < date_type.today():
                return render(request, 'book_table.html', {
                    'error': 'Please select a future date.'
                })

        except ValueError:
            return render(request, 'book_table.html', {
                'error': 'Please enter valid booking details.'
            })

        booking = TableBooking.objects.create(
            name=name,
            email=email,
            phone=phone,
            guests=guest_count,
            date=booking_date,
            time=booking_time,
            special_request=special_request
        )

        return render(request, 'booking_success.html', {
            'booking': booking
        })

    return render(request, 'book_table.html')


def Contactview(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, subject, message]):
            return render(request, 'contact.html', {
                'error': 'Please fill all the fields.'
            })

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        return render(request, 'contact.html', {
            'success': 'Your message has been submitted successfully!'
        })

    return render(request, 'contact.html')





from decimal import Decimal


def validate_customizations(item, selected_ids):
    selected_ids = list(set(selected_ids))

    options = list(
        FoodCustomization.objects.filter(
            id__in=selected_ids,
            food_item=item,
            is_active=True
        )
    )

    if len(options) != len(selected_ids):
        return None, "Invalid customization selected."

    # Check single-select groups
    selected_groups = {}

    for option in options:
        group = (option.group_name, option.selection_type)
        selected_groups.setdefault(group, []).append(option)

    for (group_name, selection_type), group_options in selected_groups.items():
        if selection_type == 'single' and len(group_options) > 1:
            return None, f"Select only one option from {group_name}."

    # Check required groups
    required_groups = (
        FoodCustomization.objects.filter(
            food_item=item,
            is_active=True,
            is_required=True
        ).values_list('group_name', flat=True).distinct()
    )

    selected_group_names = [option.group_name for option in options]

    for group_name in required_groups:
        if group_name not in selected_group_names:
            return None, f"Please select an option from {group_name}."

    return options, None


def build_cart_items(cart):
    cart_items = []
    grand_total = Decimal('0.00')
    clean_cart = {}

    for line_key, data in cart.items():

        # Old cart format compatibility
        if isinstance(data, int):
            data = {
                'food_id': line_key,
                'quantity': data,
                'customization_ids': []
            }

        try:
            food_id = int(data['food_id'])
            quantity = int(data['quantity'])
            customization_ids = [
                int(x) for x in data.get('customization_ids', [])
            ]
        except (ValueError, TypeError, KeyError):
            continue

        if quantity < 1:
            continue

        item = FoodItem.objects.filter(id=food_id).first()

        if not item:
            continue

        options = list(
            FoodCustomization.objects.filter(
                id__in=customization_ids,
                food_item=item,
                is_active=True
            )
        )

        if len(options) != len(set(customization_ids)):
            continue

        unit_price = item.price + sum(
            (option.additional_price for option in options),
            Decimal('0.00')
        )

        total_price = unit_price * quantity

        selected_customizations = [
            {
                'name': option.name,
                'group_name': option.group_name,
                'additional_price': str(option.additional_price)
            }
            for option in options
        ]

        clean_cart[line_key] = {
            'food_id': food_id,
            'quantity': quantity,
            'customization_ids': customization_ids
        }

        cart_items.append({
            'line_key': line_key,
            'item': item,
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'selected_customizations': selected_customizations
        })

        grand_total += total_price

    return cart_items, grand_total, clean_cart


@require_POST
def add_to_cart(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)

    selected_ids = request.POST.getlist('customization_ids')

    try:
        selected_ids = [int(x) for x in selected_ids]
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid customization.'
        }, status=400)

    # Fast Food aur Beverages mein default Size = Regular
    if item.category in ['Fast Food', 'Beverages']:
        size_options = FoodCustomization.objects.filter(
            food_item=item,
            group_name='Size',
            is_active=True
        )

        selected_size = FoodCustomization.objects.filter(
            id__in=selected_ids,
            food_item=item,
            group_name='Size',
            is_active=True
        ).exists()

        if not selected_size:
            regular_option = size_options.filter(name='Regular').first()

            if regular_option:
                selected_ids.append(regular_option.id)

    options, error = validate_customizations(item, selected_ids)

    if error:
        return JsonResponse({
            'success': False,
            'message': error
        }, status=400)

    selected_ids = sorted(option.id for option in options)

    line_key = f"{item.id}_{'-'.join(map(str, selected_ids)) or 'base'}"

    cart = request.session.get('cart', {})
    converted_cart = {}

    for old_key, old_value in cart.items():
        if isinstance(old_value, int):
            converted_cart[f"{old_key}_base"] = {
                'food_id': int(old_key),
                'quantity': old_value,
                'customization_ids': []
            }
        else:
            converted_cart[old_key] = old_value

    cart = converted_cart

    if line_key in cart:
        cart[line_key]['quantity'] += 1
    else:
        cart[line_key] = {
            'food_id': item.id,
            'quantity': 1,
            'customization_ids': selected_ids
        }

    request.session['cart'] = cart
    request.session.modified = True

    count = sum(data['quantity'] for data in cart.values())

    return JsonResponse({
        'success': True,
        'cart_item_count': count,
        'message': f'{item.name} added to cart!'
    })


def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items, grand_total, clean_cart = build_cart_items(cart)

    request.session['cart'] = clean_cart
    request.session.modified = True

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })


@require_POST
def remove_from_cart(request, line_key):
    cart = request.session.get('cart', {})
    cart.pop(line_key, None)

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


@require_POST
def update_cart(request, line_key):
    cart = request.session.get('cart', {})

    if line_key in cart:
        try:
            quantity = int(request.POST.get('quantity', 1))
        except (ValueError, TypeError):
            return redirect('cart')

        if quantity <= 0:
            cart.pop(line_key)
        else:
            if isinstance(cart[line_key], int):
                cart[line_key] = {
                    'food_id': line_key.split('_')[0],
                    'quantity': quantity,
                    'customization_ids': []
                }
            else:
                cart[line_key]['quantity'] = quantity

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


def checkout_view(request):
    cart = request.session.get('cart', {})

    cart_items, grand_total, clean_cart = build_cart_items(cart)

    request.session['cart'] = clean_cart
    request.session.modified = True

    if not cart_items:
        return redirect('cart')

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        if not customer_name or not phone or not address:
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'grand_total': grand_total,
                'error': 'Please fill all the details.'
            })

        if not phone.isdigit() or len(phone) != 10:
            return render(request, 'checkout.html', {
                'cart_items': cart_items,
                'grand_total': grand_total,
                'error': 'Enter a valid 10-digit mobile number.'
            })

        with transaction.atomic():
           order = Order.objects.create(
    user=request.user if request.user.is_authenticated else None,
    customer_name=customer_name,
    phone=phone,
    address=address,
    total_amount=grand_total
)

        for cart_item in cart_items:
                    OrderItem.objects.create(
                    order=order,
                    food_item=cart_item['item'],
                    item_name=cart_item['item'].name,
                    price=cart_item['unit_price'],
                    quantity=cart_item['quantity'],
                    selected_customizations=cart_item['selected_customizations']
                )

        request.session['cart'] = {}
        request.session.modified = True

        return redirect('order_success', order_id=order.id)

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'order_success.html', {
        'order': order
    })
@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related('items').order_by('-created_at')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
@require_POST
def track_recently_viewed(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)

    recently_viewed_ids = request.session.get('recently_viewed', [])

    if item_id in recently_viewed_ids:
        recently_viewed_ids.remove(item_id)

    recently_viewed_ids.insert(0, item_id)

    request.session['recently_viewed'] = recently_viewed_ids[:10]

    return JsonResponse({'success': True})


def recently_viewed(request):
    recently_viewed_ids = request.session.get('recently_viewed', [])

    items = FoodItem.objects.filter(id__in=recently_viewed_ids)

    items_by_id = {item.id: item for item in items}

    ordered_items = [
        items_by_id[item_id]
        for item_id in recently_viewed_ids
        if item_id in items_by_id
    ]

    return render(request, 'recently_viewed.html', {
        'items': ordered_items
    })
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {
        'form': form
    })