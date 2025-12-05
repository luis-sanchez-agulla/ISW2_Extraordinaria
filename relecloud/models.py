from django.db import models
from .validators import validate_image_extension, validate_image_size

# Create your models here.
class Destination(models.Model):
	name = models.CharField(
		unique=True,
		null=False,
		blank=False,
		max_length=50
	)
	description = models.TextField(
		max_length=2000,
		null=False,
		blank=False
	)
	image = models.ImageField(
		upload_to='destinations/',
		null=True,
		blank=True,
		validators=[validate_image_extension, validate_image_size],
		help_text='Formatos permitidos: JPG, JPEG, PNG, WEBP. Tamaño máximo: 20MB'
	)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return f"/destination/{self.pk}"

class Cruise(models.Model):
    name = models.CharField(
        unique=True,
        max_length=50,
        null=False,
        blank=False,
    )
    description = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    destinations = models.ManyToManyField(
        Destination,
        related_name='cruises'
    )
    def __str__(self):
        return self.name

class InfoRequest(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        blank=False,
    )
    email = models.EmailField()
    notes = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.PROTECT
    )
