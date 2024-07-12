from django.db.models import signals
from django.dispatch import receiver
from PIL import Image
from io import BytesIO
from django.core.files import File

from api.trip.models import Trip


def resize_image(image, size=(100, 60)):
    if image.width > size[0] or image.height > size[1]:
        image_filename = image.file.name
        image_extension = image.file.name.split(".")[-1]

        resized_image = Image.open(image)
        resized_image.thumbnail(size)
        buffer = BytesIO()
        resized_image.save(buffer, format=image_extension)
        return File(buffer, name=image_filename)
    return image


@receiver(signals.pre_save, sender=Trip)
def resize_trip_image_pre_save(sender, instance, **kwargs):
    default_image_name = Trip._meta.get_field("image").default
    if instance.image.name != default_image_name:
        instance.image = resize_image(instance.image)
