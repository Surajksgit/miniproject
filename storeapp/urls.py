# urls.py...............

from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="home"),
    path("signup/", views.Signuppage, name="signup"),
    path("signup/details/", views.Signupdetails, name="signupdetails"),
    path("collection/signup/", views.Signuppage, name="signup"),
    path("signup/login/", views.Loginpage, name="login"),
    path("login/details/", views.Logindetails, name="logindetails"),
    path("collection/signup/login/", views.Loginpage, name="login"),
    path("collection/", views.collection_view, name='collection'),
    path('collection/search/', views.searchi, name="search"),
    path('product_detail/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name="cart"),
    path('collection/cart/', views.cart_view, name="cart"),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('update_cart/<int:cart_id>/<str:action>/', views.update_cart, name="update_cart"),
     path('remove_from_cart/<int:cart_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout, name="checkout"),
    
]