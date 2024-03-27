from django.shortcuts import render, redirect
from .models.product import Product
from .models.category import Category
from django.http import HttpResponse
from .models.customer import Customer
from django.contrib.auth.hashers import make_password, check_password
from django.views import View


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
          
    
class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        postData = request.POST
        first_name = postData.get('first_name')
        last_name = postData.get('last_name')
        phone = postData.get('phone')  # Retrieve phone number from form data
        email = postData.get('email')
        password = postData.get('password')

        # Create customer instance
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            password=password
        )

        # Validate customer data and save if valid
        error_message = self.validateCustomer(customer)
        if not error_message:
            # Hash password before saving
            customer.password = make_password(customer.password)
            # Save customer
            customer.save()
            return redirect('homepage')
        else:
            # If there are errors, render signup page with error message
            return render(request, 'signup.html', {'error': error_message})

        
    @staticmethod
    
    def validateCustomer(customer):
        error_message = None  # Initialize error_message variable
        
        if customer:
            if not customer.first_name.strip():
                error_message = "First Name is required."
            elif not customer.last_name.strip():
                error_message = "Last Name is required."
            elif customer.phone is not None and (not customer.phone.strip() or len(customer.phone.strip()) < 11):
                error_message = "Enter a valid Phone Number (at least 11 digits)."
            elif len(customer.password) < 6:
                error_message = "Password must be at least 6 characters long."
            elif len(customer.email.strip()) < 4:
                error_message = "Email must be at least 4 characters long."
            elif customer.isExists():
                error_message = 'Email already exists.'
        else:
            error_message = "Customer information is missing."
        
        return error_message









class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    
    def post(self, request):
        postData = request.POST
        email = postData.get('email')
        password = postData.get('password')

        # Fetch customer by email
        customer = Customer.get_customer_by_email(email)
        
        if customer:
            # Check password
            if check_password(password, customer.password):
                # If password is correct, log in the customer
                request.session['customer_id'] = customer.id
                return redirect('homepage')
            else:
                # If password is incorrect, render login page with error message
                return render(request, 'login.html', {'error': 'Invalid email or password.'})
        else:
            # If customer does not exist, render login page with error message
            return render(request, 'login.html', {'error': 'Invalid email or password.'})


