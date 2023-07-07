from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpRequest
import json
from .models import *  # import tất cả code trong file models.py
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.


def message(request):
    page_current = current_page(request)
    context = {'page_current': page_current, }
    return render(request, 'app/message.html', context)

def account_setting(request):
    page_current = current_page(request)
    context = {'page_current': page_current, }
    return render(request, 'app/account_setting.html', context)

def notification(request):
    page_current = current_page(request)
    context = {'page_current': page_current,}
    return render(request, 'app/notification.html', context)


def detail(request):
    page_current = current_page(request)
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    context = {'items': items, 'order': order, 'products': products,
               'cartItems': cartItems, 'page_current': page_current}
    return render(request, 'app/detail.html', context)


def category(request):
    categories = Category.objects.filter(is_sup=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)

    context = {'categories': categories, 'products': products,
               'active_category': active_category}
    return render(request, 'app/category.html', context)


def search(request):
    page_current = current_page(request)
    if request.method == "POST":
        searched = request.POST["searched"]
        if(searched == ''): keys =''
        else:
            keys = Product.objects.filter(name__contains = searched)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

    context = {'searched': searched, 'keys': keys,
               'cartItems': cartItems, 'page_current': page_current}
    return render(request, 'app/search.html', context)


def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form': form}
    return render(request, 'app/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'user or password not correct')

    context = {}
    return render(request, 'app/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('home')

######################


def home(request):
    page_current = current_page(request)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

    categories = Category.objects.filter(is_sup=False)
    active_category = request.GET.get('category', '')
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems,
               'page_current': page_current, 'categories': categories,
               'active_category': active_category}
    return render(request, 'app/home.html', context)


def cart(request):
    page_current = current_page(request)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'page_current': page_current}
    return render(request, 'app/cart.html', context)


def checkout(request):
    page_current = current_page(request)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0, }
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'page_current': page_current}
    return render(request, 'app/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order,  product=product)

    if action == 'add':
        orderItem.quantity += 1
    if action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('updated', safe=False)
#######################################


def current_page(request: HttpRequest):
    current_path = request.path  # Đường dẫn của URL hiện tại

    # Xử lý đường dẫn để trích xuất thông tin cần thiết
    if current_path == '/':
        page = 'Trang chủ'
    elif current_path == '/cart/':
        page = 'Giỏ hàng'
    elif current_path == '/checkout/':
        page = 'Trang thanh toán'
    elif current_path == '/notification/':
        page = 'Thông báo'
    elif current_path == '/account_setting/':
        page = 'Trang cá nhân'
    elif current_path == '/message/':
        page = 'Tin nhắn'
    elif current_path == '/search/':
        page = 'Tìm kiếm'
    elif current_path.__contains__("detail"):
        page = 'Phòng trọ'
    else:
        page = ''
    return page
