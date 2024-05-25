from django.urls import path, include
from rest_framework.routers import DefaultRouter


from marketplace_app.api.views import (
    CategoryViewSet,
    ProductListAPIView,
    ProductDetailAPIView,
)

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    path('product/list/', ProductListAPIView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailAPIView.as_view(), name='product_detail'),
]
