from django.test import TestCase
from base_app.models import User
from datetime import datetime
from .models import Product, Store, Order


class ProductModelTest(TestCase):

    def test_string_representation(self):
        product = Product(product_id=1, product_description='Test Product')
        self.assertEqual(str(product), '1, Test Product')

    def test_fields(self):
        product = Product.objects.create(product_id=1, product_name='Test Product', product_code='123',
                                         product_batch=2, product_description='Test Description',
                                         product_production_date=datetime.now(),
                                         product_expiration_date=datetime.now())
        self.assertEqual(product.product_id, 1)
        self.assertEqual(product.product_name, 'Test Product')
        self.assertEqual(product.product_code, '123')
        self.assertEqual(product.product_batch, 2)
        self.assertEqual(product.product_description, 'Test Description')


class StoreModelTest(TestCase):

    def test_string_representation(self):
        store = Store(store_id=1, store_phone_number='123456789', store_trading_name='Test Store')
        self.assertEqual(str(store), 'Test Store, 123456789')

    def test_fields(self):
        user = User.objects.create(username='test_user')
        store = Store.objects.create(store_id=1, store_cnpj='123456789', store_name='Test Store',
                                     store_trading_name='Test Store', store_address='Test Address',
                                     store_email='test@example.com', store_phone_number='123456789',
                                     store_manager=user)
        self.assertEqual(store.store_id, 1)
        self.assertEqual(store.store_cnpj, '123456789')
        self.assertEqual(store.store_name, 'Test Store')
        self.assertEqual(store.store_trading_name, 'Test Store')
        self.assertEqual(store.store_address, 'Test Address')
        self.assertEqual(store.store_email, 'test@example.com')
        self.assertEqual(store.store_phone_number, '123456789')
        self.assertEqual(store.store_manager, user)


class OrderModelTest(TestCase):

    def test_string_representation(self):
        order = Order(order_id='12345')
        self.assertEqual(str(order), '12345')

    def test_fields(self):
        user = User.objects.create(username='test_user')
        store = Store.objects.create(store_id=1, store_cnpj='123456789', store_name='Test Store',
                                     store_trading_name='Test Store', store_address='Test Address',
                                     store_email='test@example.com', store_phone_number='123456789',
                                     store_manager=user)
        product = Product.objects.create(product_id=1, product_name='Test Product', product_code='123',
                                         product_batch=2, product_description='Test Description',
                                         product_production_date=datetime.now(),
                                         product_expiration_date=datetime.now())
        order = Order.objects.create(order_id='12345', store_id=store, employee_id=user, product_id=product,
                                     order_quantity=10, order_motive=1, order_confirmation_status=0)
        self.assertEqual(order.order_id, '12345')
        self.assertEqual(order.store_id, store)
        self.assertEqual(order.employee_id, user)
        self.assertEqual(order.product_id, product)
        self.assertEqual(order.order_quantity, 10)
        self.assertEqual(order.order_motive, 1)
        self.assertEqual(order.order_confirmation_status, 0)
