from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='models')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.brand.name} {self.name}'


class Car(models.Model):
    TRANSMISSION_CHOICES = [('auto', 'Автомат'), ('manual', 'Механика'), ('robot', 'Робот'), ('variator', 'Вариатор')]
    FUEL_CHOICES = [('petrol', 'Бензин'), ('diesel', 'Дизель'), ('gas', 'Газ'), ('hybrid', 'Гибрид'), ('electric', 'Электро')]
    DRIVE_CHOICES = [('fwd', 'Передний'), ('rwd', 'Задний'), ('awd', 'Полный')]
    CONDITION_CHOICES = [('new', 'Новый'), ('used', 'С пробегом')]
    COLOR_CHOICES = [('white', 'Белый'), ('black', 'Черный'), ('silver', 'Серебристый'), ('gray', 'Серый'),
                     ('red', 'Красный'), ('blue', 'Синий'), ('green', 'Зеленый'), ('brown', 'Коричневый'),
                     ('beige', 'Бежевый'), ('other', 'Другой')]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, on_delete=models.CASCADE)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=0)
    mileage = models.IntegerField(default=0)
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES)
    drive = models.CharField(max_length=10, choices=DRIVE_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default='used')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='white')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100, default='Бишкек')
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.brand} {self.model} {self.year}'

    def get_absolute_url(self):
        return reverse('cars:car_detail', kwargs={'pk': self.pk})

    def get_main_image(self):
        return self.images.first()


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='cars/')
    is_main = models.BooleanField(default=False)


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'car')


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='messages')
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender} → {self.receiver}'