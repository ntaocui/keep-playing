from django.urls import path

from . import views # imports views.py from this directory

app_name = 'sheetreader'

urlpatterns = [
	path('', views.index, name='index'),
	path('sheet/create/', views.newSheet, name='newSheet'),
    path('sheet/<int:pk>/update/', views.updateSheet, name='updateSheet'),
    path('delete/', views.deleteSheets, name='deleteSheets'),
]