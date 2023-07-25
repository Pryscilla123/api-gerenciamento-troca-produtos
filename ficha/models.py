from django.db import models

from base_app.models import User


# Create your models here.


class Product(models.Model):
    product_id = models.IntegerField(null=False, primary_key=True, auto_created=True)
    product_name = models.CharField(null=False)
    product_code = models.CharField(null=False, unique=True, max_length=255)
    product_batch = models.IntegerField(null=False)
    product_description = models.CharField(max_length=255, null=False)
    product_production_date = models.DateTimeField(null=False)
    product_expiration_date = models.DateTimeField(null=False)

    def __str__(self):
        return f'{self.product_id}, {self.product_description}'


class Store(models.Model):
    store_id = models.IntegerField(null=False, primary_key=True, auto_created=True)
    store_cnpj = models.CharField(null=False, unique=True)
    store_name = models.CharField(max_length=255, null=False)
    store_trading_name = models.CharField(max_length=255, null=False)
    store_address = models.CharField(max_length=255, null=False)
    store_email = models.EmailField(max_length=255, null=False)
    store_phone_number = models.CharField(max_length=255, null=False)
    store_manager_cpf = models.CharField(null=False)

    def __str__(self):
        return f'{self.store_trading_name}, {self.store_phone_number}'


class Order(models.Model):
    order_id = models.IntegerField(null=False, primary_key=True, auto_created=True)  # Tem que ser único, vamos fazer um hash ou o que?
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE)
    employee_cpf = models.CharField(null=False)
    store_manager_cpf = models.CharField(null=False)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_quantity = models.IntegerField(null=False)
    order_motive = models.IntegerField(null=False)  # O que será enviado para o bd é um número, que corresponde à escolha do usuário
    order_confirmation_status = models.IntegerField(null=False)  # 0 - Aguardando confirmação, 1-Confirmado, 2-Recusado
    order_creation_date = models.DateField(null=False)

    def __str__(self):
        return f'{self.order_id}'
