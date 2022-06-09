from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'internetbank'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transfer/', views.transfer, name='transfer'),
    path('transactionlist/', views.transactionlist, name='transactionlist'),
    path('balance/', views.balance, name='balance'),
    path('logout/', views.logout, name='logout'),
    path('confirm/', views.confirm, name='confirm'),
]

urlpatterns += staticfiles_urlpatterns()