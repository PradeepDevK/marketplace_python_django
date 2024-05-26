from django.urls import path, include
from rest_framework.routers import DefaultRouter


from marketplace_app.api.views import (
    CategoryViewSet,
    ProductListGenericView,
    ProductDetailGenericView,
    ProductCreateGenericView,
    products_list,
)

router = DefaultRouter()
router.register('list', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/product/', ProductListGenericView.as_view(), name='product_list'),
    path('<int:pk>/product_create/', ProductCreateGenericView.as_view(), name='product_create'),
    path('product/<int:pk>/', ProductDetailGenericView.as_view(), name='product_detail'),
    path('products/', products_list, name='products'),
]
