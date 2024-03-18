from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from django.http import HttpResponse
from .models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password


def index(request):
    products = None
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.get_all_products_by_category_id(category_id)
    else:
        products = Product.get_all_products()
    
    data = {'products': products, 'categories': categories, 'title': 'Home'}
    return render(request, 'index.html', data)

def validateCustomer(customer):
    error_message = None  # Initialize error_message variable
    if not customer.first_name or len(customer.first_name) < 2:
        error_message = "First Name is required and must be at least 2 characters long."
    elif not customer.last_name or len(customer.last_name) < 2:
        error_message = "Last Name is required and must be at least 2 characters long."
    elif not customer.phone or len(customer.phone) < 11:
        error_message = "Enter a valid Phone Number (at least 11 digits)."
    elif len(customer.password) < 6:
        error_message = "Password must be at least 6 characters long."
    elif len(customer.email) < 4:
        error_message = "Email must be 5 characters long."
    elif customer.isExists():
        error_message = 'Email already exists '
    return error_message


def registerUser(request):
    if request.method == 'POST':
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phonenumber')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        error_message = validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'value': value
            }
            return render(request, 'signup.html', data)

    # If the request method is not POST, return a redirect or render as appropriate
    return redirect('homepage')  # For example, redirect to homepage if not a POST request

            
    

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    elif request.method == 'POST':
        return registerUser(request)
    else:
        return HttpResponse("Method not allowed")
       


def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag :
                return redirect('homepage')
            else:
                error_message = 'Email or password invalid'
        else:
            error_message= 'Email or password is invalid'

        print(email,password)
        return render(request,'login.html',{'error': error_message})