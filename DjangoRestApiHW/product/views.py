from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import *
from common.permissions import IsModerator
from common.validators import validate_user_age

class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorylistSeralizer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = Category.objects.create(name=serializer.validated_data.get("name"))

        return Response(
            CategoryDetailSeralizer(category).data, status=status.HTTP_201_CREATED
        )


class CategoryDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            return None

    def get(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(
                {"error": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategoryDetailSeralizer(category)
        return Response(serializer.data)

    def put(self, request, id):
        category = self.get_object(id)
        if category is None:
            return Response(
                {"error": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategoryValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get("name")
        category.save()

        return Response(CategoryDetailSeralizer(category).data)

    def delete(self, request, id):

        category = self.get_object(id)
        if category is None:
            return Response(
                {"error": "category not found"}, status=status.HTTP_404_NOT_FOUND
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductListAPIView(APIView):
    permission_classes = [IsModerator]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductlistSeralizer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        validate_user_age(request.user)

        serializer = ProductValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = Product.objects.create(
            title=serializer.validated_data.get("title"),
            description=serializer.validated_data.get("description"),
            price=serializer.validated_data.get("price"),
            category_id=serializer.validated_data.get("category_id"),
        )

        return Response(
            ProductDetailSeralizer(product).data,
            status=status.HTTP_201_CREATED
        )


class ProductDetailAPIView(APIView):
    permission_classes = [IsModerator]

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            return None

    def get(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {"error": "product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSeralizer(product)
        return Response(serializer.data)

    def put(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {"error": "product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get("title")
        product.description = serializer.validated_data.get("description")
        product.price = serializer.validated_data.get("price")
        product.category_id = serializer.validated_data.get("category_id")
        product.save()

        return Response(ProductDetailSeralizer(product).data)

    def delete(self, request, id):
        product = self.get_object(id)
        if product is None:
            return Response(
                {"error": "product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewListAPIView(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewListSeralizer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review = Review.objects.create(
            stars=serializer.validated_data.get("stars"),
            text=serializer.validated_data.get("text"),
            product_id=serializer.validated_data.get("product_id"),
        )
        return Response(
            ReviewDetailSeralizer(review).data, status=status.HTTP_201_CREATED
        )


class ReviewDetailAPIView(APIView):

    def get_object(self, id):
        try:
            return Review.objects.get(id=id)
        except Review.DoesNotExist:
            return None

    def get(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {"error": "review not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(ReviewDetailSeralizer(review).data)

    def put(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {"error": "review not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ReviewValidationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review.stars = serializer.validated_data.get("stars")
        review.text = serializer.validated_data.get("text")
        review.product_id = serializer.validated_data.get("product_id")
        review.save()

        return Response(ReviewDetailSeralizer(review).data)

    def delete(self, request, id):
        review = self.get_object(id)
        if review is None:
            return Response(
                {"error": "review not found"}, status=status.HTTP_404_NOT_FOUND
            )
        review.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewsAPIView(APIView):

    def get(self, request):

        products = Product.objects.select_related("category").prefetch_related(
            "reviews"
        )

        serializer = ProductReviewSerializer(products, many=True)

        return Response(serializer.data)
