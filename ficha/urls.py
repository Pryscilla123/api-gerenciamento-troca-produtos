from rest_framework import routers
from ficha.views import ProductViewsSets, StoreViewsSets, OrderViewsSets, OrderGraphViewSet

router = routers.SimpleRouter()

router.register(r'produto', ProductViewsSets)
router.register(r'loja', StoreViewsSets)
router.register(r'pedidos-de-troca', OrderViewsSets) # reverse url pra pegar todos os pedidos para usário x
router.register(r'grafico-de-pedidos-de-troca', OrderGraphViewSet)

# ver necessidade de procurar os pedidos de troca

urlpatterns = router.urls
