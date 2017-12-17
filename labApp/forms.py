from django import forms
from . import models


class ProdactForm(forms.Form):
    prodact_name = forms.CharField(min_length=5, max_length=30, label='Наименование товара')
    description = forms.CharField(max_length=255, label='Описание')
    price = forms.FloatField(disabled=True, label='Цена')
    img = forms.FileField(required=False, label='Фотография')

    class Meta:
        model = models.Prodact
        fields = ('prodact_name', 'description', 'price', 'img', 'category')


class OrderForm(forms.Form):
    user = forms.CharField(disabled='True', label='Покупатель')
    prodact = forms.CharField(disabled='True', label='Продукт')
    order_date = forms.DateTimeField(widget=forms.SelectDateWidget(), label='Дата заказа')
    number = forms.IntegerField(disabled=True, label='Количество')

