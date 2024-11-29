from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Incluindo as URLs da aplicação 'stats'
    path('', include('stats.urls')),  # Isso vai carregar as URLs definidas em 'stats/urls.py'
]
