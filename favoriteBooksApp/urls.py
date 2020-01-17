from django.urls import path     
from . import views
urlpatterns = [
path('', views.register),
path('createuser', views.createuser),
path('login', views.login),
path ('book',views.book),
path('addBook', views.add),
path ('show/<bookId>', views.display),
path('book/<bookId>/delete', views.delete),
path('edit/<bookId>/edit', views.edit),
path('update/<bookId>', views.update),
path('book/<bookId>/addfavor', views.addfavor),
path('book/<bookId>/removefavor', views.removefavor),
path('logout',views.logout),
]