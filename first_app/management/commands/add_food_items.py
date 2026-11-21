
from django.core.management.base import BaseCommand
from first_app.models import FoodItem


class Command(BaseCommand):
    help = 'Add FoodZone menu items'

    def handle(self, *args, **kwargs):

        items = [
            ('French Fries', 'Crispy golden potato fries served with tasty seasoning.', 249, 'Fast Food', 'img/french_fries.jpg'),
            ('Veg Sandwich', 'Fresh vegetable sandwich with cheese and special sauce.', 99, 'Fast Food', 'img/veg_sandwich.jpg'),
            ('White Sauce Pasta', 'Creamy pasta prepared with white sauce and fresh herbs.', 129, 'Fast Food', 'img/white_sauce_pasta.jpg'),
            ('Garlic Bread', 'Toasted garlic bread topped with butter and herbs.', 199, 'Fast Food', 'img/garlic_bread.jpg'),

            ('Paneer Butter Masala', 'Soft paneer cooked in rich and creamy tomato gravy.', 149, 'Main Course', 'img/paneer_butter_masala.jpg'),
            ('Veg Biryani', 'Aromatic basmati rice cooked with fresh vegetables and spices.', 229, 'Main Course', 'img/veg_biryani.jpg'),
            ('Dal Makhani', 'Traditional creamy dal cooked with butter and Indian spices.', 179, 'Main Course', 'img/dal_makhani.jpg'),
            ('Shahi Paneer', 'Delicious paneer cooked in rich royal-style gravy.', 199, 'Main Course', 'img/shahi_paneer.jpg'),
            ('Chole Bhature', 'Spicy chickpeas served with soft and fluffy bhature.', 269, 'Main Course', 'img/chole_bhature.jpg'),
            ('Special Thali', 'Complete Indian meal served with delicious traditional dishes.', 149, 'Main Course', 'img/special_thali.jpg'),

            ('Cold Coffee', 'Chilled coffee blended with milk and creamy texture.', 249, 'Beverages', 'img/cold_coffee.jpg'),
            ('Chocolate Shake', 'Rich chocolate milkshake served chilled.', 99, 'Beverages', 'img/chocolate_shake.jpg'),
            ('Mango Shake', 'Fresh mango blended with chilled milk.', 129, 'Beverages', 'img/mango_shake.jpg'),
            ('Fresh Lime Soda', 'Refreshing lime drink with soda and fresh mint.', 129, 'Beverages', 'img/fresh_lemonade.jpg'),
            ('Strawberry Shake', 'Delicious strawberry shake blended with chilled milk.', 79, 'Beverages', 'img/strawberry_shake.jpg'),
            ('Masala Chai', 'Traditional Indian tea brewed with aromatic spices.', 159, 'Beverages', 'img/masala_chai.jpg'),
        ]

        added = 0

        for name, description, price, category, image in items:
            obj, created = FoodItem.objects.get_or_create(
                name=name,
                defaults={
                    'description': description,
                    'price': price,
                    'category': category,
                    'image': image,
                }
            )

            if created:
                added += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'{added} new food items added successfully!'
            )
        )
