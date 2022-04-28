from django.shortcuts import render, redirect
from tomlkit import item
from .models import Category, Food, Order, OrderItem, Delivery
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json


# Create your views here.
def home(request):
    featured_foods = Food.objects.filter(featured=True)
    context = {
        'featured_foods': featured_foods,
    }
    return render(request, "main/home.html", context)

def menu(request):
    searchQuery = ''
    category = ''
    if request.GET.get("searchQuery"):
        searchQuery = request.GET.get("searchQuery")
    foods = Food.objects.filter(name__icontains=searchQuery)
    categories = Category.objects.all()
    if request.GET.get("category"):
        category = request.GET.get("category")
        foods = Food.objects.filter( category__tag__contains=category )
    context = {
        'foods':foods,
        'categories' : categories,
        'searchQuery': searchQuery,
    }
    return render(request, "main/menu.html", context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,status="Pending")
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print(cart)
        items = []
        order = {
            'get_cart_total' : 0,
            'get_cart_item' : 0,
        }
        cartItem = order['get_cart_item']
        for i in cart:
            cartItem += cart[i]['quantity']
            food = Food.objects.get(id=i)
            total = (food.price *cart[i]['quantity'])
            order['get_cart_item'] += cart[i]['quantity']
            order['get_cart_total'] += total
            print(order['get_cart_item'] )
            item = {
                'food':{
                    'id':food.id,
                    'name':food.name,
                    'price': food.price,
                    'imageURL':food.imageURL,
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)
        
    context = {
        'items' : items,
        'order' : order,
    }

    return render(request, "main/cart.html", context)


    

def updateItem(request):
    data = json.loads(request.body)
    foodId = data['foodId']
    action = data['action']
    customer = request.user
    food = Food.objects.get(id=foodId)
    order, created = Order.objects.get_or_create(customer=customer,status="Pending")

    orderItem, created = OrderItem.objects.get_or_create(order=order, food=food)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
        messages.success(request, f"{orderItem.food.name} was added to cart sucessfully.")
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        messages.warning(request, f"{orderItem.food.name} was removed from cart")

    return JsonResponse("The item was added", safe=False)

@login_required(login_url='login')
def orders(request):
    if request.user.is_authenticated:
        customer = request.user
        orders = Order.objects.filter(customer=customer).exclude(status="Pending")
    context = {
        'orders' : orders
    }

    return render(request, "main/orders.html", context)

@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer,status="Pending")
        items = order.orderitem_set.all()
    else:
        items = []
        order = {
            'get_cart_total' : 0
        }
    context = {
        'items' : items,
        'order' : order
    }

    return render(request, "main/checkout.html", context)


def process_order(request):
    data = json.loads(request.body)
    customer = request.user
    order, created = Order.objects.get_or_create(customer=customer,status="Pending")

    order.status="Ordered"    

    order.save()
    return render(request,'main/orders.html',{})

def cancel(request):
    data = json.loads(request.body)
    orderId = data['orderId']
    food = data['item']
    order = Order.objects.get(transaction_id=orderId)
    item = OrderItem.objects.get(order=order, food=food)
    item.delete()
    return JsonResponse("Order cancelled", safe=False)
    
