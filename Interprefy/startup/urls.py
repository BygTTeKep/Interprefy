from django.urls import path, include
from .views import (
    client_registration,
    ajax_send_pin,
    detail_client,
    intermediary_registration,
    detail_intermediary,
    top_intermediares,
    add_products_intermediary,
    loginpage,
    main,
)
from django.conf import settings
from django.conf.urls.static import static



app_name = 'interprefy'

urlpatterns = [
    path('Interprefy', main, name='Interprefy'),



    path('client/registration/', client_registration, name='client_registration'),
    path('client/<slug:slug>/', detail_client, name='client_detail'),
    path('ajax_send_pin', ajax_send_pin, name='ajax_send_pin'),
    path('intermediary/registration/',intermediary_registration, name='intermediary_registration'),
    path('intermediary/<slug:slug>/', detail_intermediary, name='detail_intermediary'),
    path('intermediary/<slug:slug>/add-products', add_products_intermediary, name='add_product'),
    path('top', top_intermediares, name='top'),
    path('accounts/login/', loginpage, name='login')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
