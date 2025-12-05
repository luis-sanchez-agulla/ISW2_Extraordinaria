from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from .validators import validate_image_extension, validate_image_size, validate_image_dimensions

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
        validators=[
            validate_image_extension,
            validate_image_size,
            validate_image_dimensions
        ],
        help_text='Formato: JPG, PNG o WEBP. Máximo 5MB. Dimensiones: 300x300 a 2000x2000 píxeles'
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


class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Muy malo'),
        (2, '2 - Malo'),
        (3, '3 - Regular'),
        (4, '4 - Bueno'),
        (5, '5 - Excelente'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    cruise = models.ForeignKey(
        Cruise,
        on_delete=models.CASCADE,
        related_name='reviews',
        null=True,
        blank=True
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        choices=RATING_CHOICES
    )
    title = models.CharField(
        max_length=200,
        null=False,
        blank=False
    )
    comment = models.TextField(
        max_length=2000,
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = [['user', 'destination'], ['user', 'cruise']]
    
    def __str__(self):
        if self.destination:
            return f"Reseña de {self.user.username} sobre {self.destination.name}"
        return f"Reseña de {self.user.username} sobre {self.cruise.name}"
