import io
from django.db import models
from src.accounts.models import User
from django.core.files.base import ContentFile
# barcode module, which is used for generating various types of barcodes in Python.
import barcode
from barcode import EAN13, UPCA
# ImageWriter is responsible for generating barcode images.
from barcode.writer import ImageWriter
# BytesIO provides a binary stream interface for in-memory byte buffers.
from io import BytesIO
from django.core.files import File
from src.core.modules import upload_barcode_path

class Barcode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="barcodes")
    product = models.OneToOneField(
        "Product", on_delete=models.CASCADE, related_name="barcode"
    )
    value = models.CharField(max_length=250, unique=True)

    image = models.ImageField(upload_to=upload_barcode_path, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"({self.product.name}) - {self.value}"
    
    def save(self, *args, **kwargs):
        # Call the parent save method to get the instance saved first
        super().save(*args, **kwargs)
        
        # Generate the barcode using the provided value
        UPCA = barcode.get_barcode_class('ean13')
        upca = UPCA(self.value, writer=ImageWriter(), guardbar=True)

        # Save the barcode image to a BytesIO object with the text option
        buffer = io.BytesIO()
        # options={'write_text': True, 'text_distance': 2}
        options={'module_height': 10, 'text_distance': 2}

        upca.write(buffer, options)
        
        # Save the buffer content to the image field of the Barcode model
        image_name = f'barcode_{self.pk}.png'
        self.image.save(image_name, ContentFile(buffer.getvalue()), save=False)
        
        # Call the parent save method again to save the image field
        super().save(*args, **kwargs)