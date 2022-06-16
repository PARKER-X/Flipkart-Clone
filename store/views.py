from django.shortcuts import render
from .models import *
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
import datetime
from django.views.generic import ListView , DetailView 
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def store(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer = customer, complete = False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items

    # else:
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
    #     cartItems = order['get_cart_items']
    
  
    
    

    products = Product.objects.all()
    books = Product.objects.filter(category='Book')
    foods = Product.objects.filter(category='Food')
    cloths = Product.objects.filter(category='Cloth')
    
    paginator = Paginator(cloths, 3)
    paginator2 = Paginator(books, 3)
    paginator3 = Paginator(foods, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    page_number = request.GET.get('page')
    page_obj2 = paginator2.get_page(page_number)

    page_number = request.GET.get('page')
    page_obj3 = paginator3.get_page(page_number)

    context = {'products':products, 'books':books, 'foods':foods, 'cloths':cloths, 'page_obj': page_obj, 'page_obj2': page_obj2, 'page_obj3': page_obj3}

    return render(request, 'store/index.html', context)




    


def Books(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    books = Product.objects.filter(category='Book')

    context = {'products':products, 'books':books,'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'store/book.html', context)

def Foods(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    foods = Product.objects.filter(category='Food')

    context = {'products':products, 'foods':foods,'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'store/food.html', context)

def Cloths(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    cloths = Product.objects.filter(category='Cloth')

    context = {'products':products, 'cloths':cloths,'items':items, 'order':order, 'cartItems':cartItems}

    return render(request, 'store/cloth.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0,'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']
    
    context = {'items':items, 'order':order ,'cartItems':cartItems,'shipping':False}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('productId:', productId)
    print('action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action== 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transcation_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        total = data['form']['total']
        order.transcation_id = transcation_id

        if total == order.get_cart_total:
            order.complete = True 
        order.save()

        if order.shipping==True:
            ShippingAddress.objects.create(customer=customer, order=order, address=data['shipping']['address'], city=data['shipping']['city'] , state=data['shipping']['state'], zipcode = data['shipping']['zipcode'],)
    
    else:
        print('User is not logged in..')
    return JsonResponse('Payment complete!', safe=False)


def product_detail(request, pk):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    post = Product.objects.get(id=pk)



    return render(request, 'store/detail.html', {'post': post, "cartItems":cartItems })