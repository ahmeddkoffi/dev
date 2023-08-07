#devproject/urls.py
from django.contrib import admin
from django.urls import path
from myapp import views  
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'), 
    path('all_events/', views.all_events, name='all_events'), 
    path('add_event/', views.add_event, name='add_event'), 
    path('update/', views.update, name='update'),
    path('remove_event/', views.remove_event, name='remove_event'),
    path('prediction/', views.prediction, name='prediction'),  # Nouvelle route pour la vue "prédiction"
]