
from django.core.management.base import BaseCommand
from first_app.models import FoodItem


class Command(BaseCommand):
    help = "Update images for 30 new FoodZone items"

    def handle(self, *args, **kwargs):

        items = [
            'Paneer Pizza', 'Mexican Burger', 'Cheese Burst Sandwich',
            'Veg Spring Roll', 'Peri Peri Fries', 'Schezwan Noodles',
            'Paneer Momos', 'Cheese Corn Balls', 'Tandoori Paneer Wrap',
            'Veg Manchurian Dry', 'Malai Kofta', 'Paneer Lababdar',
            'Mushroom Masala', 'Veg Handi', 'Dum Aloo', 'Kadhi Pakora',
            'Masala Dosa', 'Veg Hakka Noodles', 'Chole Bhature',
            'Punjabi Kadhi Rice', 'Blue Lagoon', 'Virgin Pina Colada',
            'Watermelon Juice', 'Pineapple Juice', 'Cold Chocolate',
            'KitKat Shake', 'Rose Milk', 'Badam Milk',
            'Peach Iced Tea', 'Hot Chocolate'
        ]

        updated = 0

        for name in items:
            item = FoodItem.objects.filter(name=name).first()

            if item:
                filename = name.lower().replace(' ', '_') + '.jpg'
                item.image = f'img/{filename}'
                item.save(update_fields=['image'])
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'{updated} food item images updated successfully!'
        ))
