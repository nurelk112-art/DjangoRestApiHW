from django.urls import path
from product import views

urlpatterns = [
    path("categories/", views.CategoryListAPIView.as_view()),
    path("categories/<int:id>/", views.CategoryDetailAPIView.as_view()),
    path("products/", views.ProductListAPIView.as_view()),
    path("products/<int:id>/", views.ProductDetailAPIView.as_view()),
    path("reviews/", views.ReviewListAPIView.as_view()),
    path("reviews/<int:id>/", views.ReviewDetailAPIView.as_view()),
    path("products/reviews/", views.ProductReviewsAPIView.as_view()),
]
