
from django.core.management.base import BaseCommand
from first_app.models import FoodItem


class Command(BaseCommand):
    help = "Add 30 more FoodZone menu items"

    def handle(self, *args, **kwargs):

        items = [
            # FAST FOOD
            ('Paneer Pizza', 'Delicious pizza topped with spicy paneer and cheese.', 249, 'Fast Food', 'img/cheese_pizza.jpg'),
            ('Mexican Burger', 'Burger with a spicy Mexican-style vegetable patty.', 189, 'Fast Food', 'img/classic_burger.jpg'),
            ('Cheese Burst Sandwich', 'Grilled sandwich loaded with melted cheese.', 169, 'Fast Food', 'img/veg_sandwich.jpg'),
            ('Veg Spring Roll', 'Crispy rolls stuffed with seasoned vegetables.', 139, 'Fast Food', 'img/veg_sandwich.jpg'),
            ('Peri Peri Fries', 'Crispy fries tossed in peri peri seasoning.', 159, 'Fast Food', 'img/french_fries.jpg'),
            ('Schezwan Noodles', 'Spicy noodles tossed with Schezwan sauce.', 169, 'Fast Food', 'img/veg_fried_rice.jpg'),
            ('Paneer Momos', 'Soft dumplings filled with spicy paneer.', 149, 'Fast Food', 'img/veg_sandwich.jpg'),
            ('Cheese Corn Balls', 'Crispy golden balls filled with cheese and corn.', 159, 'Fast Food', 'img/french_fries.jpg'),
            ('Tandoori Paneer Wrap', 'Wrap filled with smoky tandoori paneer.', 189, 'Fast Food', 'img/veg_sandwich.jpg'),
            ('Veg Manchurian Dry', 'Crispy vegetable balls tossed in Manchurian sauce.', 179, 'Fast Food', 'img/veg_fried_rice.jpg'),

            # MAIN COURSE
            ('Malai Kofta', 'Soft vegetable dumplings in creamy gravy.', 199, 'Main Course', 'img/shahi_paneer.jpg'),
            ('Paneer Lababdar', 'Paneer cooked in rich tomato and cashew gravy.', 219, 'Main Course', 'img/paneer_butter_masala.jpg'),
            ('Mushroom Masala', 'Fresh mushrooms cooked in Indian masala gravy.', 199, 'Main Course', 'img/shahi_paneer.jpg'),
            ('Veg Handi', 'Mixed vegetables cooked in traditional handi gravy.', 189, 'Main Course', 'img/special_thali.jpg'),
            ('Dum Aloo', 'Baby potatoes cooked in aromatic Indian gravy.', 169, 'Main Course', 'img/dal_makhani.jpg'),
            ('Kadhi Pakora', 'Traditional yogurt curry served with pakoras.', 149, 'Main Course', 'img/dal_makhani.jpg'),
            ('Masala Dosa', 'Crispy dosa filled with spiced potato masala.', 129, 'Main Course', 'img/special_thali.jpg'),
            ('Veg Hakka Noodles', 'Stir-fried noodles with fresh vegetables.', 159, 'Main Course', 'img/veg_fried_rice.jpg'),
            ('Chole Bhature', 'Spicy chickpea curry served with fluffy bhature.', 179, 'Main Course', 'img/special_thali.jpg'),
            ('Punjabi Kadhi Rice', 'Punjabi kadhi served with steamed rice.', 159, 'Main Course', 'img/jeera_rice.jpg'),

            # BEVERAGES
            ('Blue Lagoon', 'Refreshing blue citrus cooler served chilled.', 109, 'Beverages', 'img/fresh_lemonade.jpg'),
            ('Virgin Pina Colada', 'Creamy pineapple and coconut cooler.', 139, 'Beverages', 'img/mango_shake.jpg'),
            ('Watermelon Juice', 'Fresh watermelon juice served chilled.', 89, 'Beverages', 'img/fresh_lemonade.jpg'),
            ('Pineapple Juice', 'Fresh pineapple juice with a tropical taste.', 99, 'Beverages', 'img/mango_shake.jpg'),
            ('Cold Chocolate', 'Chilled chocolate drink with a creamy texture.', 119, 'Beverages', 'img/chocolate_shake.jpg'),
            ('KitKat Shake', 'Thick milkshake blended with KitKat chocolate.', 159, 'Beverages', 'img/chocolate_shake.jpg'),
            ('Rose Milk', 'Chilled milk flavoured with sweet rose syrup.', 89, 'Beverages', 'img/strawberry_shake.jpg'),
            ('Badam Milk', 'Creamy milk flavoured with almonds and saffron.', 99, 'Beverages', 'img/mango_shake.jpg'),
            ('Peach Iced Tea', 'Refreshing iced tea with peach flavour.', 109, 'Beverages', 'img/mint_mojito.jpg'),
            ('Hot Chocolate', 'Warm chocolate drink topped with creamy foam.', 129, 'Beverages', 'img/chocolate_shake.jpg'),
        ]

        added = 0
        existing = 0

        for name, description, price, category, image in items:
            _, created = FoodItem.objects.get_or_create(
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
            else:
                existing += 1

        self.stdout.write(self.style.SUCCESS(
            f'{added} new items added, {existing} already existed.'
        ))
