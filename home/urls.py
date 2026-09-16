from django.urls import path
from .views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('acessar', IndexView.as_view(), name='accessar'),
]