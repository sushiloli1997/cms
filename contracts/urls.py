from django.urls import path

from . import views
from django.contrib.auth.views import LogoutView




urlpatterns = [
    path('change-password/', views.change_password, name='change-password'),
    path('roles/', views.Role.as_view(), name='roles'),
    path('users/', views.userlist, name='users'),
    path('users/<int:pk>', views.delete_user, name='delete-user'),
    path('', views.login_view, name='login'),
    path('report/', views.report, name='report'),
    # path('web/', views.web_index, name='web'),
    path('add_clients/', views.add_clients, name='add-clients'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_company/', views.add_company, name='add-company'),
    path('company_list/', views.company_list, name='company_list'),
    path('delete_contract/<int:pk>', views.delete_contract, name='delete_contract'),
    path('edit_company/<int:pk>', views.edit_company, name='edit_company'),
    path('contract/', views.contract, name='contract-list'),
    path('add_contract/', views.add_contract, name='add_contract'),
    path('view-contract/<int:pk>/', views.contract_view, name='view-contract'),
    path('icons/', views.icons_view, name='icons'),
    path('create-user/', views.user_create, name='create-user'),
    path('delete-company/<int:pk>', views.delete_company, name='delete-company'),
    path('approve-contract/<int:contract_id>/', views.approve_contract,  name='approve-contract'),
    path('add-comission/<int:contract_id>/', views.add_comission,  name='add-comission'),
    path('reject-contract/<int:contract_id>/', views.reject_contract,  name='reject-contract'),
    path('update-payment-status/<int:contract_id>/', views.update_payment_status,  name='update-payment-status'),
    path('add-comment/<int:contract_id>/', views.add_comment,  name='add-comment'),
    path('client-profile/<int:pk>/', views.client_profile,  name='client-profile'),
    path('search/', views.search,  name='search'), # type: ignore
    path('compare/<int:contract_id>', views.compare_amount,  name='compare'),
    path('profile/', views.profile, name='profile'),
    path('export-to-csv', views.Json_Test, name='export-to-csv')
]