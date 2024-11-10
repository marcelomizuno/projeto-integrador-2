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
    path('get_user_data/<int:user_id>/', views.get_user_data, name='get_user_data'),
    path('save_user/', views.save_user, name='save_user'),
    path('export_users/', views.export_users, name='export_users'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('save_product/', views.save_product, name='save_product'),
    path('get_product_data/<int:product_id>/', views.get_product_data, name='get_product_data'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
]


# Configurações de templates de erro
handler404 = 'app_name.views.custom_404'
handler500 = 'app_name.views.custom_500'
handler403 = 'app_name.views.custom_403'
handler400 = 'app_name.views.custom_400'