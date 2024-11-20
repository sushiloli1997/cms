from django import views
from django.urls import path
from . import views

urlpatterns= [
    path('', views.invoice, name='invoice'), # type: ignore
    path('new-index/', views.new_index, name='new_index'), # type: ignore
    path('alpine_test/', views.new_index, name='new_index'), # type: ignore
    path('delete-invoice/<int:pk>', views.delete_invoice, name='delete-invoice'),
    path('view_invoice/<int:pk>', views.view_invoice, name='view-invoice'),
    path('add-invoicetracks/<int:pk>', views.add_invoicetracks, name='add-invoicetracks'), # type: ignore

]
