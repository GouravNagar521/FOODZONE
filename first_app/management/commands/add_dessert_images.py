
from django.core.management.base import BaseCommand
from first_app.models import FoodItem


class Command(BaseCommand):
    help = "Update images for FoodZone desserts"

    def handle(self, *args, **kwargs):

        desserts = {
            'Gulab Jamun': 'img/gulab_jamun.jpg',
            'Rasmalai': 'img/rasmalai.jpg',
            'Rasgulla': 'img/rasgulla.jpg',
            'Chocolate Brownie': 'img/chocolate_brownie.jpg',
            'Chocolate Lava Cake': 'img/chocolate_lava_cake.jpg',
            'Black Forest Pastry': 'img/black_forest_pastry.jpg',
            'Red Velvet Pastry': 'img/red_velvet_pastry.jpg',
            'Cheesecake': 'img/cheesecake.jpg',
            'Chocolate Ice Cream': 'img/chocolate_ice_cream.jpg',
            'Vanilla Ice Cream': 'img/vanilla_ice_cream.jpg',
            'Strawberry Ice Cream': 'img/strawberry_ice_cream.jpg',
            'Kesar Kulfi': 'img/kesar_kulfi.jpg',
            'Rice Kheer': 'img/rice_kheer.jpg',
            'Gajar Ka Halwa': 'img/gajar_ka_halwa.jpg',
            'Fruit Cream': 'img/fruit_cream.jpg',
        }

        updated = 0
        missing = []

        for name, image_path in desserts.items():
            count = FoodItem.objects.filter(
                name=name,
                category="Desserts"
            ).update(image=image_path)

            if count:
                updated += count
            else:
                missing.append(name)

        self.stdout.write(
            self.style.SUCCESS(
                f"Updated {updated} dessert images."
            )
        )

        if missing:
            self.stdout.write(
                self.style.WARNING(
                    "Not found: " + ", ".join(missing)
                )
            )
