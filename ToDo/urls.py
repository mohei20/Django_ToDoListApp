from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='todo-index'),
    path('add', views.add_task, name='add-task'),
    path('update/<int:pk>/', views.update, name='update'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('login/', views.loginpage, name='todo-login'),
    path('register/', views.registerpage, name='todo-register'),
    path('logout/', views.lougoutuser, name='todo-logout'),
    path('search/', views.search, name='search'),
    path('completed/', views.show_completed, name='todo-completed'),
    path('uncompleted/', views.show_uncompleted, name='todo-uncompleted'),
    #path('calendar/<int:year>/<str:month>/', views.calendar, name='todo-calendar'),
]