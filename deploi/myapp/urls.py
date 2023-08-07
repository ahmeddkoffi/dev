# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.afficher_calendrier, name='afficher_calendrier'),
    path('add_event/', views.add_event, name='add_event'),  # Nouvelle URL pour la vue add_event
    path('', views.chart, name='chart')
]

#path('enregistrer-prix/<int:jour_id>/', views.enregistrer_prix, name='enregistrer_prix'),
