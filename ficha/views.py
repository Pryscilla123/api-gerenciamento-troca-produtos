from enum import Enum

import datetime
from django.utils.dateparse import parse_date, parse_datetime
from django.db.models import Q, Count
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ViewDoesNotExist
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from base_app.permissions.user_permissions import IsRepositorGroupPermission, IsRepresentanteDeLojaGroupPermission, \
    IsAdminGroupPermission
from ficha.models import Product
from ficha.models import Store
from ficha.models import Order

from ficha.serializers import ProductSerializer, OrderGraphicSerializer
from ficha.serializers import StoreSerializer
from ficha.serializers import OrderSerializer


# Create your views here.


class AccessLevel(Enum):
    REPOSITOR = 1
    ADMIN = 2
    REPRESENTANTE = 3


class ProductViewsSets(viewsets.ModelViewSet):

    """
    Rota de Produtos.

    product_id -> Id do produto (automático)
    product_name -> Nome do produto
    product_code -> Código de barras do produto
    product_batch -> Lote a qual o produto pertence
    product_description -> Descrição do produto
    product_production_date -> Data de fábricação do produto
    product_expiration_date -> Data de vencimento do produto
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    lookup_field = 'product_code'

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            permission_classes = [IsAdminGroupPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsRepositorGroupPermission]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class StoreViewsSets(viewsets.ModelViewSet):

    """
    Rota de Lojas.

    store_id -> Id da loja (gerado automáticamente)
    store_cnpj -> CNPJ da loja
    store_name -> Nome real da loja
    store_trading_name -> Nome fantasia da loja
    store_address -> Endereço da loja
    store_email -> E-mail da loja
    store_phone_number -> Telofone da loja
    store_manager_cpf -> CPF do representante de loja
    """

    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    lookup_field = 'store_cnpj'

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            permission_classes = [IsAdminGroupPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsRepositorGroupPermission]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]


class OrderViewsSets(viewsets.ModelViewSet):
    """
    Rota de Pedido de troca.

    order_id -> Id do pedido de troca (gerado automáticamente)
    store_id -> Id da loja que quer efetuar o pedido
    employee_cpf -> CPF do repositor
    store_manager_cpf -> CPF do representante de loja
    product_id -> Id do produto para a troca
    order_quantity -> Quantidade do produto a ser trocado
    order_motive -> Motivo para a troca
    order_confirmation_status -> Status de confirmação do pedido de troca
    order_creation_date -> Data de criação do pedido de troca
    """
    queryset = Order.objects.all()

    serializer_class = OrderSerializer

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'update':
            permission_classes = [IsRepositorGroupPermission]
        elif self.action == 'retrieve':
            permission_classes = [IsRepresentanteDeLojaGroupPermission, IsRepositorGroupPermission]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        """
        Rota de listagem dos pedidos de troca.

        Nessa rota os pedidos são filtrados de acordo com o usuário logado.

        Os pedidos, caso não específicado a data retorna os pedidos do dia.

        Para filtrar dois parametros devem ser adicionados:
            - date: Data do pedido de troca
            - store_id: Id da loja
        """
        user = self.request.user
        date = self.request.query_params.get('date', None)  # order_creation_data
        store_id = self.request.query_params.get('store_id', None)

        if date:
            queryset = Order.objects.filter(order_creation_date=datetime.datetime.strptime(date, '%Y-%m-%d')).all()
        else:
            queryset = Order.objects.filter(order_creation_date=datetime.datetime.now()).all()

        if user.nivel_acesso == AccessLevel.REPOSITOR.value:
            queryset = Order.objects.filter(employee_cpf=user.cpf).all()
        elif user.nivel_acesso == AccessLevel.REPRESENTANTE.value:
            queryset = Order.objects.filter(store_manager_cpf=user.cpf).all()

        if store_id:
            is_manager = all([True if obj.store_id.store_manager_cpf == user.cpf else False for obj in
                              Order.objects.filter(store_id=store_id).all()])
            if user.nivel_acesso == AccessLevel.REPRESENTANTE.value and is_manager:
                queryset = Order.objects.filter(store_id=store_id).all()
            elif user.nivel_acesso == AccessLevel.REPOSITOR.value:
                queryset = Order.objects.filter(store_id=store_id).all()
            else:
                raise ViewDoesNotExist('Representante de loja sem acesso a essa loja')

        return Response(self.serializer_class(queryset, many=True).data,
                        status=status.HTTP_200_OK)


class OrderGraphViewSet(RetrieveModelMixin, GenericViewSet):

    """
    Rota para geração dos gráficos.

    Parâmetro: Data e mês no formato %Y-%m.
    Retorno: Número de ocorrências por empresa.
    """

    queryset = Order.objects.all()
    serializer_class = OrderGraphicSerializer
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _get_objects_by_year_month(date):
        objects = Order.objects.filter(order_creation_date__year=date.year, order_creation_date__month=date.month).all()
        return objects

    @staticmethod
    def _get_count_motives(objects):
        motives = ['Vencimento', 'Avaria', '0800', 'RECALL']
        store_dict = {store.store_id.store_name:{motive:0 for motive in motives} for store in objects}

        for object in objects:
            store_dict[object.store_id.store_name][motives[object.order_motive]] += 1

        return store_dict

    def retrieve(self, request, *args, **kwargs):
        date = datetime.datetime.strptime(kwargs.get('pk'), '%Y-%m')
        objects = self._get_objects_by_year_month(date)
        motives = self._get_count_motives(objects)
        # serializer = OrderGraphicSerializer(data=motives)

        return Response(motives, status=status.HTTP_200_OK)
