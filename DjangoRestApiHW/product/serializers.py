from pydoc import describe
from unicodedata import category

from rest_framework import serializers
from .models import Category, Product, Review
from rest_framework.exceptions import ValidationError

class CategorylistSeralizer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields = "name products_count".split()

    def get_products_count(self, obj):
        return obj.products.count()


class CategoryDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewListSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "text stars".split()


class ReviewDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductlistSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "title price".split()


class ProductDetailSeralizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductReviewSerializer(serializers.ModelSerializer):
    category = CategorylistSeralizer(read_only=True)
    reviews = ReviewListSeralizer(read_only=True, many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = "title price reviews category rating".split()

    def get_rating(self, obj):
        reviews = obj.reviews.all()

        if not reviews:
            return 0

        return sum(r.stars for r in reviews) / reviews.count()


class ProductValidationSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(min_length=2, max_length=255)
    price = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise serializers.ValidationError("category not found")

        return category_id


class CategoryValidationSerializer(serializers.Serializer):
    name = serializers.CharField(min_length=2, max_length=100)

    def validate_name(self, name):
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Category already exists")
        return name


class ReviewValidationSerializer(serializers.Serializer):
    stars = serializers.IntegerField()
    text = serializers.CharField(min_length=5, max_length=500)

    product_id = serializers.IntegerField()

    def validate_stars(self, stars):
        if stars < 1 or stars > 5:
            raise serializers.ValidationError("Stars must be between 1 and 5")
        return stars

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return product_id
