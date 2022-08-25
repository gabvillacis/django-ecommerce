from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse
from .models import *
from .forms import SignUpForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import json
from .cart import Cart
from django.db import transaction

def index(request):
    products = Product.objects.all()
    return render(request, 'store.html', {'products': products})

def product_detail(request, product_id):
    if product_id>25:
        raise Http404('The product does not exist')
    else:
        context = {'productId': product_id}
        return render(request, 'product_detail.html', context)

def cart(request):
    shopping_cart = Cart(request)
    total_cart = sum(item['subtotal'] for item in shopping_cart)
    return render(request, 'cart.html', context = {'shopping_cart': shopping_cart, 'total_cart': total_cart})

def checkout(request): 
    shopping_cart = Cart(request)
    total_cart = sum(item['subtotal'] for item in shopping_cart)    
    return render(request, 'checkout.html', context = {'shopping_cart': shopping_cart, 'total_cart': total_cart})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "Se ha registrado exitosamente.") 
            return redirect("index")

    form = SignUpForm()
    return render(request, 'signup.html', context = { 'signup_form': form })

def login_view_function(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"Ha iniciado sesión exitosamente como: {username}.")
                return redirect("index")
            else:
                messages.error(request, "Usuario o contraseña inválidos.")
        else:
            messages.error(request, "Usuario o contraseña inválidos.")
    
    form = AuthenticationForm()
    return render(request, "login.html", context={'login_form': form})

def logout_view_function(request): 
    logout(request)
    messages.info(request, "Ha cerrado la sesión exitosamente.") 
    return redirect("index")

def add_item_to_cart(request):
    cart = Cart(request)

    data = json.loads(request.body)
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity'))
    get_object_or_404(Product, id=product_id)
    
    cart.add(product_id, quantity)
    return JsonResponse({"added": True, "total_items": cart.__len__()})

def remove_item_from_cart(request):    
    cart = Cart(request)
    data = json.loads(request.body)
    product_id = int(data.get('product_id'))

    cart.delete(product_id=product_id)
    return JsonResponse({"deleted": True, "total_items": cart.__len__()})


@transaction.atomic
def process_order(request):
    try:
        if request.method == "POST":
            
            cart = Cart(request)

            data = json.loads(request.body)
            identification = data.get('identification')
            full_name = data.get('full_name')
            email = data.get('email')
            city = data.get('city')
            address = data.get('address')
            cellphone = data.get('cellphone')
            cart_total = sum(item.get('subtotal') for item in cart)

            print('Los campos recibidos son: ', data)
            print('Los items del carrito son: ', cart.__len__())

            try:
                customer = Customer.objects.get(identification=identification)
                customer.full_name = full_name
                customer.email = email
                customer.phone = cellphone
                customer.save(update_fields=['full_name', 'email', 'phone'])
            except Customer.DoesNotExist:
                customer = Customer(user=request.user,
                                    identification=identification,
                                    full_name=full_name,
                                    email=email,
                                    phone=cellphone)
                customer.save()

            order = Order(  customer=customer,
                            complete=True,
                            total=cart_total)
            order.save()

            for item in cart:
                order_item = OrderItem( order=order,
                                        product=item.get('product'),
                                        quantity=item.get('quantity'))
                order_item.save()

            shippingAddress = ShippingAddress(  order=order,
                                                city=city,
                                                address=address,
                                                phone=cellphone)
            shippingAddress.save()
            
            cart.clear()
            return JsonResponse({"order_id": order.id}, status=201)
    except Exception as error:
        print('Ocurrió un error al generar el pedido: ', repr(error))
        return JsonResponse({"error_msg": "Opps, su pedido no pudo ser ingresado. " + repr(error)}, status=500)