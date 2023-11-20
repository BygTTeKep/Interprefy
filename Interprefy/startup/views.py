from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
# from .tasks import sms_send, _verify_pin
from django.views.decorators.http import require_GET
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth import get_user_model
import random
from django.conf import settings# SMSAERO_EMAIL, SMSAERO_API_KEY
from django.db.models import Subquery
from smsaero import SmsAero
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .forms import (ClientForm,
                    IntermediaresForm,
                    AddProductForm,
                    
                    )
from .models import (CUser, 
                     Posts,
                     Products,
                     Categories,
                     )
User = get_user_model()


def _verify_pin(mobile_number, pin):
    """ Verify a PIN is correct """
    return pin == cache.get(mobile_number)

def _get_pin(length=6):
    """ Return a numeric PIN with length digits """
    return random.sample(range(10**(length-1), 10**length), 1)[0]


def main(request:HttpRequest):
    '''
        дефолтный all() с сортировкой по коментариям оценкам
    '''
    # context = {
    #     'top_intermediares': CUser.objects.filter().all().order_by()
    # }
    return render(request, 'startup/main.html', {})



# @require_GET
# def main_view(request: HttpRequest) -> HttpResponse:
#     # context = {
#     #     'subscriptions': Subscription.objects.filter(Subscribe_client_id=id).select_related(Clients).select_related(Intermediares),
#     #     'posts': Intermediares.objects.filter(Subscribe_intermediary_id=Subscription.objects.filter(Subscribe_client_id=id).get('Subscribe_intermediary_id')),
#     #     'posts':Intermediares.objects.raw(f'''SELECT text_post, Intermediares.Name FROM Posts
#     #                                         INNER JOIN Intermediares ON Posts.posts_intermediary_id = Intermediares.id 
#     #                                         INNER JOIN Subscription  ON Subscription.Subscribe_intermediary_id = Intermediares.id
#     #                                         INNER JOIN Clients ON Subscription.Subscribe_client_id = Clients.id
#     #                                         WHERE Subscribe_client_id = {id}'''),
#     # }
#     return render(request, "startup/main.html", {})

@csrf_exempt
def ajax_send_pin(request: HttpRequest):
    """ Sends SMS PIN to the specified number """
    mobile_number = request.POST.get('mobile_number', "")
    if not mobile_number:
        return HttpResponse("No mobile number", mimetype='text/plain', status=403)

    pin = _get_pin()

    # store the PIN in the cache for later verification.
    cache.set(mobile_number, pin, 5*60) 

    api = SmsAero(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)
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
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                login(request, user=user)
                return redirect('interprefy:client_detail', slug=user.username)
            else:
                cache.delete(telephone_number)
                messages.error(request, "Invalid PIN")
        else: messages.error(request, form.errors)
    else:
        context = {
            "form": ClientForm()
        }
        return render(request, "startup/client_reg.html", context)

@require_GET
def detail_client(request:HttpRequest, slug):
    context = {
        'users': CUser.objects.get(UserSlug=slug)
    }
    return render(request, 'startup/detail_client.html', context)

def intermediary_registration(request:HttpRequest):
    if request.method == "POST":
        form = IntermediaresForm(request.POST or None)
        if form.is_valid():
            intermediary = form.save(commit=False)
            intermediary.is_intermediary = True
            intermediary.user_permissions.set(['add_posts', 'change_posts', 'delete_posts', 'view_posts',
                                               'add_products', 'change_products', 'delete_products', 'view_products',
                                               ])
            intermediary.save()
            return redirect('Interprefery:detail_intermediary', slug=intermediary.username)
        else:
            messages.error(request, form.errors)
            return render(request, 'startup/intermediary_reg.html', {'form':IntermediaresForm(request.POST)})#<================
    else:
        context = {
            "form": IntermediaresForm()
        }
        return render(request, 'startup/intermediary_reg.html', context)
    
# @login_required
# @permission_required(perm=['add_post', 'change_post', 'delete_post'])

def detail_intermediary(request:HttpRequest, slug):
    '''
        Отображает все товары, магазины, страны откуда/в поставки/доставка
        Информация о посреднике
    '''
    # a = CUser.objects.raw(f'''SELECT id FROM CUser WHERE UserSlug={slug}''')
    intermediary_id = CUser.objects.filter(UserSlug=slug).only("id")
    context = {
        'intermediaries': CUser.objects.get(UserSlug=slug),
        'products': Products.objects.filter(IntermediaryID=Subquery(intermediary_id))
        # 'products': Products.objects.select_related(Categories).select_related(CUser).filter(UserSlug=slug).get(id)
    }
    return render(request, 'startup/detail_intermediary.html', context)

def top_intermediares(request:HttpRequest):
    context = {
        'intermediares': CUser.objects.filter(is_intermediary=True).all()
    }
    return render(request, 'startup/top_intermediary.html', context)

@login_required
def add_products_intermediary(request:HttpRequest, slug):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            messages.info(request, 'created')
            product = form.save(commit=False)
            product.IntermediaryID = CUser.objects.get(UserSlug=slug)
            product.save()
            return redirect('interprefy:add_product')
        else:
            messages.info(request, form.errors)
    else:
        context = {
            'form': AddProductForm()
        }
        return render(request, 'startup/add_products_intermediary.html', context)
    
def loginpage(request:HttpRequest):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user=user)
            return render(request, 'startup/login.html', {})
    else:
        return render(request, 'startup/login.html', {})
    return render(request, 'startup/login.html', {})
