from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.timezone import now


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Покупатель')

    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    birthday = models.DateField(verbose_name='День рождения')
    sex = models.CharField(max_length=1, verbose_name='Пол')
    img = models.ImageField(upload_to='user/', blank=True, default='user/user_icon.png',
                          verbose_name='Фотография')

    objects = models.Manager()

    #def __str__(self):
     #   return "{}".format(self.user)

    def __str__(self):
        return "{}".format(self.user.username)



class ProdactCategory(models.Model):
    category_name = models.CharField(max_length=30, verbose_name='Категория товара')

    objects = models.Manager()

    def __str__(self):
        return "{}".format(self.category_name)

class ProdactManager(models.Manager):

    def get_all_trans(self, user_id):
        return Prodact.objects.filter(user=user_id)

class Prodact(models.Model):
    prodact_name = models.CharField(max_length=30, verbose_name='Наименование товара')
    description = models.CharField(max_length=255, null=True, verbose_name='Описание')
    price = models.FloatField(max_length=10, verbose_name='Цена')
    img = models.ImageField(upload_to='prodact/', blank=True,
                           default='prodact/prodact_icon.png', verbose_name='Фотография')
    category = models.ManyToManyField(ProdactCategory, blank=True, verbose_name='Категория товара')

    objects = ProdactManager()

    def __str__(self):
        return "{} {}".format(self.prodact_name, self.description)




class Order(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='Покупатель')
    prodact = models.ForeignKey(Prodact, on_delete=models.CASCADE, verbose_name='Продукт')
    order_date = models.DateField(default=now, blank=False, verbose_name='Дата заказа')
    number = models.IntegerField(default=1, blank=False, verbose_name='Количеcтво')

    objects = models.Manager()

    class Meta:
        ordering = ('-order_date',)

    def __str__(self):
        return "{}: {} {}".format(self.user.user.username, self.order_date)