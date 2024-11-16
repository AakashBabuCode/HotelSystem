from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Existing routes
    path('', views.login_register_view, name='login_register'),  # Login/Register Page
    path('home/', views.home_view, name='home'),  # Home Page after login
    path('logout/', views.logout_view, name='logout'),  # Logout View
    path('add_product/', views.add_product, name='add_product'),
    # Cart functionality routes
    path('menu/', views.menu_view, name='menu'),
    path('add_to_cart/<str:product_id>/', views.add_to_cart, name='add_to_cart'),  # Add to cart
    path('view_cart/', views.view_cart, name='view_cart'),  # View cart
    
    # Checkout (if you implement it later)
    # path('checkout/', views.checkout_view, name='checkout'),  # Checkout Page
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)