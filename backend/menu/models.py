from django.db import models

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('juices', 'Juices'),
        ('snacks', 'Snacks'),
        ('beverages', 'Beverages'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='snacks')
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)
    
    def __str__(self):
        return self.name