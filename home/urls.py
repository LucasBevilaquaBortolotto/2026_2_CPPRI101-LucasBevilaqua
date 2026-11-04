from django.urls import path
from .views import HomeView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('login/', LoginView.as_view(template_name='login.html',extra_context={'titulo': 'Autenticação'}), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('alterar-senha/', PasswordChangeView.as_view( template_name='login.html',extra_context={'titulo': 'Alterar Senha'},success_url=reverse_lazy('home')), name='alterar_senha'),
]