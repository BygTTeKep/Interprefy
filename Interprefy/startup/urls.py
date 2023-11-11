from django.urls import path
from .views import (
    client_registration,
    ajax_send_pin,
)



app_name = 'interprefy'

urlpatterns = [
    path('client/registration/', client_registration, name='client_registration'),
    path('ajax_send_pin', ajax_send_pin, name='ajax_send_pin'),
]
