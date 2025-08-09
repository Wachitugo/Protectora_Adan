from django.urls import path
from . import views

app_name = 'donaciones'

urlpatterns = [
    path('donar/', views.donar, name='donar'),
    path('gracias/<int:donacion_id>/', views.gracias, name='gracias'),
    path('avisos/', views.avisos, name='avisos'),
    path('webpay/resultado/', views.webpay_resultado, name='webpay_resultado'),
    path('webpay/error/', views.webpay_error, name='webpay_error'),
    path('webpay/test/', views.test_webpay_config, name='test_webpay'),
]
