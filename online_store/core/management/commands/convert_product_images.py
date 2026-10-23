from pathlib import Path

from django.core.management.base import BaseCommand

from core.images import as_webp
from core.models import productImage


class Command(BaseCommand):
    help = "Convert existing product images to WebP and update their database paths."

    def handle(self, *args, **options):
        converted = 0
        skipped = 0

        for product_image in productImage.objects.iterator():
            field = product_image.image
            if not field or Path(field.name).suffix.lower() == ".webp":
                skipped += 1
                continue

            old_name = field.name
            with field.storage.open(old_name, "rb") as source:
                converted_file = as_webp(source)

            # save() selects a collision-safe name and updates the database.
            field.save(converted_file.name, converted_file, save=True)
            if old_name != field.name:
                field.storage.delete(old_name)
            converted += 1
            self.stdout.write(f"{old_name} -> {field.name}")

        self.stdout.write(self.style.SUCCESS(
            f"Converted {converted} product image(s); skipped {skipped} WebP image(s)."
        ))
