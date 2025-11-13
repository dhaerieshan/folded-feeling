from django.urls import path
from . import views

urlpatterns = [
    path('adminpage/', views.admin_page, name='admin_page'),
    path('', views.proposal_page, name='proposal_page'),
]