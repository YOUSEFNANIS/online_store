from io import BytesIO
from pathlib import Path

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


WEBP_QUALITY = 82


def as_webp(image_file):
    """Return an uploaded image as an optimized WebP Django file."""
    image_file.seek(0)
    with Image.open(image_file) as source:
        image = ImageOps.exif_transpose(source)
        image.load()

        # WebP supports RGB and alpha. Palette/grayscale inputs need conversion
        # so Pillow does not retain an inefficient or unsupported source mode.
        has_alpha = image.mode in ("RGBA", "LA") or (
            image.mode == "P" and "transparency" in image.info
        )
        image = image.convert("RGBA" if has_alpha else "RGB")

        output = BytesIO()
        image.save(output, format="WEBP", quality=WEBP_QUALITY, method=6)

    stem = Path(image_file.name).stem or "image"
    return ContentFile(output.getvalue(), name=f"{stem}.webp")
