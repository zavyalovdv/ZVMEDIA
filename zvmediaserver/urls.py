from django.urls import path
from zvmediaserver import views

urlpatterns = [
    path('books/', views.show_books),
    path('', views.index, name='home'),
]
