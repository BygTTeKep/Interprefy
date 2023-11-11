from django.shortcuts import render

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
# from .tasks import sms_send, _verify_pin
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.core.cache import cache
import random
from Interprefy.settings import SMSAERO_EMAIL, SMSAERO_API_KEY
from smsaero import SmsAero
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import (ClientForm,
                    IntermediaresForm,
                    )
from .models import (Clients, 
                     Intermediares, 
                     Subscription, 
                     Posts)


def _verify_pin(mobile_number, pin):
    """ Verify a PIN is correct """
    return pin == cache.get(mobile_number)

def _get_pin(length=6):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]



@csrf_exempt
def ajax_send_pin(request: HttpRequest):
    """ Sends SMS PIN to the specified number """
    mobile_number = request.POST.get('mobile_number', "")
    if not mobile_number:
        return HttpResponse("No mobile number", mimetype='text/plain', status=403)

    pin = _get_pin()

    # store the PIN in the cache for later verification.
    cache.set(mobile_number, pin, 5*60) 

    api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
    res = api.send(mobile_number, f"{pin}")
    return HttpResponse("Message sent", status=200)


def client_registration(request: HttpRequest):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name= str(request.POST.get('FullName')).split()[0]
            user.last_name= str(request.POST.get('FullName')).split()[1]
            user.MiddleName=str(request.POST.get('FullName')).split()[2]
            user.save()
            pin = int(request.POST.get("pin", 0))
            telephone_number = request.POST.get("mobile_number", "")
            if _verify_pin(telephone_number, pin):
                form.save()
                return redirect('test_startapp:client_detail', kwargs={'slug', user.username})
            else:
                cache.delete(telephone_number)
                messages.error(request, "Invalid PIN")
        else: messages.error(request, form.errors)
    else:
        context = {
            "form": ClientForm()
        }
        return render(request, "test_startapp/client_reg.html", context)
