import graphene

from .models import Category, Product
from .types import CategoryType, ProductType

class CreateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        name = graphene.String()

    @staticmethod
    def mutate(root, info, **kwargs):
        name = kwargs.get('name', '').strip()
        category = Category.objects.create(name=name)
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):
    category = graphene.Field(CategoryType)

    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String(required=True)

    @staticmethod
    def mutate(root, info, **kwargs):
        cid = int(kwargs.get('cid', ''))
        category = Category.objects.get(pk=cid)

        category.name = kwargs.get('name', category.name).strip()
        category.save()
        return UpdateCategoryMutation(category)

class DeleteCategoryMutation(graphene.Mutation):
    status = graphene.String(required=True)
    message = graphene.String(required=True)

    class Arguments:
        cid = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, **kwargs):
        cid = int(kwargs.get('cid', ''))
        category = Category.objects.get(pk=cid)
        try:
            category.delete()
            return DeleteCategoryMutation(
                status='success',
                message='Category removed successfully'
            )
        except Exception as err:
            return DeleteCategoryMutation(status='error', message=err)

class CreateProductMutation(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        code = graphene.String()
        name = graphene.String()
        price = graphene.Float()
        qty = graphene.Int()
        categories_id = graphene.List(graphene.Int)
    
    @staticmethod
    def mutate(root, info, **kwargs):
        code = kwargs.get('code', '').strip()
        name = kwargs.get('name', '').strip()
        price = float(kwargs.get('price', 0.0))
        qty = int(kwargs.get('qty', 0))
        categories_id = kwargs.get('categories_id', [])

        product = Product.objects.create(
            code=code,
            name=name,
            price=price,
            qty=qty
        )

        categories = [Category.objects.get(pk=c_id) for c_id in categories_id]
        product.categories.set(categories)

        return CreateProductMutation(product)

class UpdateProductMutation(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        pid = graphene.Int(required=True)
        code = graphene.String()
        name = graphene.String()
        price = graphene.Float()
        qty = graphene.Int()
        categories_id = graphene.List(graphene.Int)
    
    @staticmethod
    def mutate(root, info, **kwargs):
        pid = int(kwargs.get('pid'))

        product = Product.objects.get(pk=pid)
        product.code = kwargs.get('code', product.code).strip()
        product.name = kwargs.get('name', product.name).strip()
        product.price = float(kwargs.get('price', product.price))
        product.qty = int(kwargs.get('qty', product.qty))
        product.save()

        if categories_id := kwargs.get('categories_id'):
            categories = [Category.objects.get(pk=c_id) for c_id in categories_id]
            product.categories.set(categories)

        return UpdateProductMutation(product)

class DeleteProductMutation(graphene.Mutation):
    status = graphene.String(required=True)
    message = graphene.String(required=True)

    class Arguments:
        pid = graphene.Int(required=True)

    @staticmethod
    def mutate(root, info, **kwargs):
        pid = int(kwargs.get('pid'))
        product = Product.objects.get(pk=pid)
        try:
            product.delete()
            return DeleteProductMutation(
                status='success',
                message='Product removed successfully'
            )
        except Exception as err:
            return DeleteProductMutation(status='error', message=err)
