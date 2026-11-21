
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg, Count
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.db.models.functions import TruncMonth

from first_app.models import FoodItem, Order, ContactMessage, TableBooking


@staff_member_required(login_url='/admin/login/')
def dashboard_home(request):
    monthly_sales = (
    Order.objects.filter(status='Delivered')
    .annotate(month=TruncMonth('created_at'))
    .values('month')
    .annotate(
        revenue=Sum('total_amount'),
        orders=Count('id')
    )
    .order_by('month')
)

    context = {
        'total_food': FoodItem.objects.count(),
        'total_orders': Order.objects.count(),
        'total_messages': ContactMessage.objects.count(),
        'total_bookings': TableBooking.objects.count(),
        'monthly_sales': monthly_sales,

        'recent_orders': Order.objects.order_by('-created_at')[:5],
        'recent_bookings': TableBooking.objects.order_by('-created_at')[:5],
        'total_revenue': Order.objects.filter(status='Delivered').aggregate(total=Sum('total_amount'))['total'] or 0,

'delivered_orders': Order.objects.filter(status='Delivered').count(),

'pending_orders': Order.objects.filter(status='Pending').count(),

'average_order_value': Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0,
    }

    return render(request, 'dashboard_app/dashboard.html', context)


@staff_member_required(login_url='/admin/login/')
def orders_view(request):

    orders = Order.objects.all().order_by('-created_at')

    return render(request, 'dashboard_app/orders.html', {
        'orders': orders
    })


@staff_member_required(login_url='/admin/login/')
@require_POST
def update_order_status(request, order_id):

    order = get_object_or_404(Order, id=order_id)
   
    new_status = request.POST.get('status')

    valid_statuses = ['Pending', 'Confirmed', 'Delivered', 'Cancelled']

    if new_status in valid_statuses:
        order.status = new_status
        order.save()

    return redirect('dashboard_orders')
@staff_member_required(login_url='/admin/login/')
def food_items_view(request):

    foods = FoodItem.objects.all().order_by('category', 'name')

    search = request.GET.get('search', '')
    category = request.GET.get('category', '')

    if search:
        foods = foods.filter(name__icontains=search)

    if category:
        foods = foods.filter(category=category)

    return render(request, 'dashboard_app/food_items.html', {
        'foods': foods,
        'search': search,
        'selected_category': category
    })
@staff_member_required(login_url='/admin/login/')
def add_food_view(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.POST.get('image')

        FoodItem.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )

        return redirect('dashboard_food_items')

    return render(request, 'dashboard_app/add_food.html')
@staff_member_required(login_url='/admin/login/')
def edit_food_view(request, food_id):

    food = get_object_or_404(FoodItem, id=food_id)

    if request.method == 'POST':
        food.name = request.POST.get('name')
        food.description = request.POST.get('description')
        food.price = request.POST.get('price')
        food.category = request.POST.get('category')
        food.image = request.POST.get('image')

        food.save()

        return redirect('dashboard_food_items')

    return render(request, 'dashboard_app/edit_food.html', {
        'food': food
    })


@staff_member_required(login_url='/admin/login/')
@require_POST
def delete_food_view(request, food_id):

    food = get_object_or_404(FoodItem, id=food_id)
    food.delete()

    return redirect('dashboard_food_items')
@staff_member_required(login_url='/admin/login/')
def bookings_view(request):

    bookings = TableBooking.objects.all().order_by('-created_at')

    return render(request, 'dashboard_app/bookings.html', {
        'bookings': bookings
    })
@staff_member_required(login_url='/admin/login/')
def messages_view(request):

    messages = ContactMessage.objects.all().order_by('-created_at')

    return render(request, 'dashboard_app/messages.html', {
        'messages': messages
    })