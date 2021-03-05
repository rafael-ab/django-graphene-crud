import graphene

from django.core.exceptions import ObjectDoesNotExist

from .models import Category, Product
from .types import CategoryType, ProductType

class CategoryQuery(object):
    category = graphene.Field(
        CategoryType,
        id=graphene.Int()
    )
    categories = graphene.List(CategoryType)

    def resolve_categories(self, info, **kwargs):
        return Category.objects.all()
    
    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')

        if id:
            try:
                return Category.objects.get(pk=id)
            except Category.DoesNotExist:
                return None
        else:
            return None

class ProductQuery(object):
    product = graphene.Field(
        ProductType,
        id=graphene.Int(),
        code=graphene.String()
    )
    products = graphene.List(ProductType)
    
    def resolve_product(self, info, **kwargs):
        id = kwargs.get('id')
        code = kwargs.get('code')

        if id:
            try:
                return Product.objects.get(pk=id)
            except Product.DoesNotExist:
                return None
        elif code:
            try:
                return Product.objects.get(code=code)
            except Product.DoesNotExist:
                return None
        else:
            return None

    def resolve_products(self, info, **kwargs):
        return Product.objects.all()
    