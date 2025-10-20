from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.fazer_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('resetar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('resetar-senha/sucesso/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('resetar-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('resetar-senha/completo/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('solicitar-permissao-professor/', views.solicitar_permissao_professor, name='solicitar_permissao_professor'),
    path('gerenciar-solicitacoes-professor/', views.gerenciar_solicitacoes_professor, name='gerenciar_solicitacoes_professor'),
]