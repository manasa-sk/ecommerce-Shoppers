from . import views
from .views import Page
from django.urls import path

urlpatterns = [
    path('home/', Page.home, name='home'),
    path('shop/', Page.shop, name='shop'),
    path('about/', Page.about, name='about'),
    path('contact/', Page.contact, name='contact'),
    path('product/', Page.product_dis, name='product-display'),
    path('checkout/', Page.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('log/', Page.loginPage, name='login'),
    path('register/', Page.registerPage, name='register'),
    path('loginUser/', views.loginUser, name='loginUser'),
    path('registerUser/', views.registerUser, name='registerUser'),
    path('addToCart/', views.addToCart, name='add'),
    path('cart/', views.cart, name='cart'),
    path('remove/', views.removeItem, name='remove'),
    path('orderplaced/', views.Page.thankyou, name='order_placed'),
    path('filter/', views.filter, name='filter'),
    path('account/', views.Page.account, name='account'),
    path('order/', views.Page.showOrder, name='orderDet'),
    path('logout/', views.logout, name='logout'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)