from rest_framework import serializers
from rest_framework import serializers
from ficha.models import Product, Store, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id',
                  'product_name',
                  'product_code',
                  'product_batch',
                  'product_description',
                  'product_production_date',
                  'product_expiration_date']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_id',
                  'store_cnpj',
                  'store_name',
                  'store_trading_name',
                  'store_address',
                  'store_email',
                  'store_phone_number',
                  'store_manager_cpf']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_id', 
                  'store_id', 
                  'employee_cpf',
                  'store_manager_cpf',
                  'product_id', 
                  'order_quantity', 
                  'order_motive',
                  'order_confirmation_status',
                  'order_creation_date']


class OrderGraphicSerializer(serializers.Serializer):

    data = serializers.DictField(required=True)
