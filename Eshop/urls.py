"""Eshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('cart/', views.cartDetails),
    path('checkout/', views.checkoutDetails),
    path('login/',views.loginDetails),
    path('product/<int:num>/', views.productDetails),
    path('contact/',views.contactDetails),
    path('shop/<str:cat>/<str:br>/', views.shopDetails),
    path('signup/', views.signupUser),
    path('profile/', views.profile),
    path('logout/', views.logout),
    path('addproduct/',views.addProduct),
    path('deleteproduct/<int:num>/',views.deleteProduct),
    path('editproduct/<int:num>/',views.editProduct),
    path('deletecart/<int:num>/',views.deleteProduct),
    path('confirm/',views.confirm),
    path('wishlist/<int:num>/',views.wishlistDetails),
    path('wishlist/',views.wishlistBuyer),
    path('deletewishlist/<int:num>/',views.wishlistDelete),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
