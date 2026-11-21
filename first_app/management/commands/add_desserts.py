
from django.core.management.base import BaseCommand
from first_app.models import FoodItem


class Command(BaseCommand):
    help = "Add 15 dessert items to FoodZone"

    def handle(self, *args, **kwargs):

        desserts = [
            ("Gulab Jamun", "Soft khoya dumplings soaked in sugar syrup.", 79),
            ("Rasmalai", "Soft paneer discs served in creamy saffron milk.", 99),
            ("Rasgulla", "Soft and spongy cottage cheese balls in sugar syrup.", 69),
            ("Chocolate Brownie", "Rich and fudgy chocolate brownie.", 119),
            ("Chocolate Lava Cake", "Warm chocolate cake with a molten centre.", 149),
            ("Black Forest Pastry", "Chocolate pastry layered with cream and cherries.", 99),
            ("Red Velvet Pastry", "Soft red velvet pastry with cream frosting.", 119),
            ("Cheesecake", "Creamy cheesecake with a biscuit base.", 159),
            ("Chocolate Ice Cream", "Classic rich chocolate ice cream.", 79),
            ("Vanilla Ice Cream", "Classic smooth vanilla ice cream.", 59),
            ("Strawberry Ice Cream", "Sweet and creamy strawberry ice cream.", 79),
            ("Kesar Kulfi", "Traditional Indian kulfi flavoured with saffron.", 69),
            ("Rice Kheer", "Traditional rice pudding cooked in milk.", 89),
            ("Gajar Ka Halwa", "Carrot pudding prepared with milk and nuts.", 99),
            ("Fruit Cream", "Seasonal fruits mixed with sweet cream.", 109),
        ]

        added = 0
        existing = 0

        for name, description, price in desserts:
            _, created = FoodItem.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "price": price,
                    "category": "Desserts",
                    "image": "",
                },
            )

            if created:
                added += 1
            else:
                existing += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Desserts complete: {added} added, {existing} already existed."
            )
        )
