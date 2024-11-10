from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


# Configurações de templates de erro
handler404 = 'app_name.views.custom_404'
handler500 = 'app_name.views.custom_500'
handler403 = 'app_name.views.custom_403'
handler400 = 'app_name.views.custom_400'