from django.urls import path
from . import views

urlpatterns=[
    path('', views.board, name='task'),
    path('board/<int:id>', views.view_board, name='view_board'),
    path("printers/", views.get_printers_and_status, name="printers"),
    path("print/", views.print_file, name="print_file"),
    path("prints/", views.upload_for_print, name="print_file"),
    path('move_card/<int:id>/', views.move_card, name='move-card'),
]
