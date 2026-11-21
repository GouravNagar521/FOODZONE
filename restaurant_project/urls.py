"""
URL configuration for restaurant_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from dashboard_app import views as dashboard_views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from first_app.views import (
    Homeview, Aboutview, Menuview, Booktableview, Contactview,
    add_to_cart, cart_view, remove_from_cart, update_cart,
    checkout_view, order_success,my_orders,track_recently_viewed, recently_viewed,register_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', dashboard_views.dashboard_home, name='dashboard_home'),
    path('dashboard/orders/', dashboard_views.orders_view, name='dashboard_orders'),
path('dashboard/food-items/add/', dashboard_views.add_food_view, name='add_food'),
path('register/', register_view, name='register'),
path('dashboard/messages/', dashboard_views.messages_view, name='dashboard_messages'),
path('dashboard/food-items/edit/<int:food_id>/', dashboard_views.edit_food_view, name='edit_food'),
path(
    'dashboard/orders/update/<int:order_id>/',
    dashboard_views.update_order_status,
    name='update_order_status'
),
path('my-orders/', my_orders, name='my_orders'),
path('recently-viewed/', recently_viewed, name='recently_viewed'),
path('recently-viewed/track/<int:item_id>/', track_recently_viewed, name='track_recently_viewed'),
path(
    'login/',
    auth_views.LoginView.as_view(template_name='login.html'),
    name='login'
),
path(
    'logout/',
    auth_views.LogoutView.as_view(next_page='/'),
    name='logout'
),

path(
    'dashboard/bookings/',
    dashboard_views.bookings_view,
    name='dashboard_bookings'
),
    path('', Homeview),
    path('book_table/', Booktableview),
    path('menu/', Menuview, name='menu'),
    path('about/', Aboutview),
    path('contact/', Contactview),
    path('cart/', cart_view, name='cart'),
    path('dashboard/food-items/delete/<int:food_id>/', dashboard_views.delete_food_view, name='delete_food'),
    path('dashboard/food-items/', dashboard_views.food_items_view, name='dashboard_food_items'),
path('cart/add/<int:item_id>/', add_to_cart, name='add_to_cart'),
path('cart/remove/<str:line_key>/', remove_from_cart, name='remove_from_cart'),
path('cart/update/<str:line_key>/', update_cart, name='update_cart'),
path('checkout/', checkout_view, name='checkout'),
path('order-success/<int:order_id>/', order_success, name='order_success'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)