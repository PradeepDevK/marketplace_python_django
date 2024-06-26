from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.exceptions import ValidationError, NotFound

from marketplace_app.api.serializer import (
    CategorySerializer,
    ProductSerializer
)
from marketplace_app.models import (
    Category,
    Product,
)
from marketplace_app.api.permissions import (
    IsAdminOrReadOnlyPermission,
    IsAuthUserOrReadOnlyPermission,
    IsAdminOrReadOnlyGroupPermission,
)
from marketplace_app.api.pagination import (
    ProductListPagination,
    ProductListOffsetPagination
)



"""
class ProductListGenericView
"""
class ProductListGenericView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductListOffsetPagination
    # filter_backends = [DjangoFilterBackend]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['title', 'description']
    search_fields = ['title', 'description']
    ordering_fields = ['created']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Product.objects.filter(category=pk)
    

"""
class ProductDetailGenericView
"""
class ProductDetailGenericView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthUserOrReadOnlyPermission]
    

"""
class ProductCreateGenericView
"""    
class ProductCreateGenericView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def queryset(self):
        return Product.objects.all()
    
    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        try :
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound("Category does not exist.")
        
        product_user = self.request.user
        
        serializer.save(category=category, product_user=product_user)
        
    
"""
Get Products
"""
@api_view(['GET'])
def products_list(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
            

"""
Viewsets for the categories
"""
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminOrReadOnlyPermission]
    permission_classes = [IsAdminOrReadOnlyGroupPermission]
    