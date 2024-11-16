# myproject/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Default admin page
    path('', include('accounts.urls')),  # Include the URLs from the 'accounts' app
]
