from django.urls import path
from . import views

urlpatterns = [
     path('', views.index , name='index'),
     path('login' , views.signin , name='login'),
     path('logout', views.logout_usr , name='logout'),
     path('change-password/<token>/', views.change_password , name='change-password'),
     path('forget-password', views.forget_password , name='forget-password'),
     path('signup', views.signup ,name='signup'),
     path('token' , views.token_send , name='token_send'),
     path('success', views.success , name='success'),
     path('error', views.error , name='error'),
     path('verify/<token>/', views.verify , name='verify' ),
     path('movie/<str:pk>/' , views.movie ,name='movie'),
     path('genre/<str:pk>/' , views.genere ,name='genre'),
     path('mylist', views.my_list, name='mylist'),
     path('add-to-list', views.add_to_list , name='add-to-list'),
     path('search' , views.search , name='search'),
     
]