from django.urls import path
from accounts import views

app_name ='accounts'

urlpatterns = [
    path('', views.index, name='index'),

    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('requests/', views.RequestListView.as_view(), name='request-list'),
    path('requests/new/', views.RequestCreateView.as_view(), name='request-create'),
    path('requests/<int:pk>/delete/', views.RequestDeleteView.as_view(), name='request-delete'),
]