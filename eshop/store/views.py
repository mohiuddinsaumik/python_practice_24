from django.shortcuts import render
from .models.product import Product
from .models.category import Category
from django.http import HttpResponse
from .models.customer import Customer

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

def signup(request):
    if request.method == 'GET':
        return render(request,'signup.html')
    
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phonenumber')
        email = postData.get('email')
        password = postData.get('password')

        # Validation
        error_message = None

        if not first_name or len(first_name) < 2:
            error_message = "First Name is required and must be at least 2 characters long."
        elif not last_name or len(last_name) < 2:
            error_message = "Last Name is required and must be at least 2 characters long."
        elif not phone or len(phone) < 11:
            error_message = "Enter a valid Phone Number (at least 11 digits)."
        elif len(password) < 6:
            error_message = "Password must be at least 6 characters long."
            


    
        # Saving
        if not error_message:
            customer = Customer(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                password=password
            )
            customer.register()
        else:
            return render(request, 'signup.html', {'error': error_message})

        return HttpResponse("Successfully Signed Up")
            
    




    data = {'title': 'Sign up'}
       