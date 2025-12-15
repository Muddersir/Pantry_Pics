from django.urls import path
from .views import (
    CategoryListView, ProductListCreateView, ProductRetrieveUpdateDestroyView,
    AddToWishlistView, WishlistListView, RemoveFromWishlistView,
    CreateReviewView, ReviewDetailView, ProductDetailWithRatingView
)

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("", ProductListCreateView.as_view(), name="product-list-create"),
    path("<int:pk>/", ProductRetrieveUpdateDestroyView.as_view(), name="product-detail"),
    path("<int:pk>/detail/", ProductDetailWithRatingView.as_view(), name="product-detail-rating"),
    path("wishlist/", WishlistListView.as_view(), name="wishlist-list"),
    path("wishlist/add/", AddToWishlistView.as_view(), name="wishlist-add"),
    path("wishlist/<int:pk>/remove/", RemoveFromWishlistView.as_view(), name="wishlist-remove"),
    path("<int:pk>/reviews/add/", CreateReviewView.as_view(), name="review-add"),
    path("reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
]