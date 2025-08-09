from django.urls import path
from . import views

app_name = 'adopciones'

urlpatterns = [
    path('', views.lista_perros, name='lista_perros'),
    path('perro/<int:perro_id>/', views.detalle_perro, name='detalle_perro'),
    path('perro/<int:perro_id>/solicitar/', views.solicitar_adopcion, name='solicitar_adopcion'),
]
