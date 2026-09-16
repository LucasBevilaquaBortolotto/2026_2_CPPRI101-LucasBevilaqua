from django.urls import path
from .views import FilmeView, FilmeAddView

urlpatterns = [
    path('filme', FilmeView.as_view(), name='filme'),
    path('filme/novo/', FilmeAddView.as_view(), name='filme_novo'),
]