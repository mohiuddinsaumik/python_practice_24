from django.shortcuts import render
from .models.product import Product
from .models.category import Category

def index(request):
    products = None
    categories = Category.get_all_categories()
    category_id = request.GET.get('category')
    
    if category_id:
        products = Product.get_all_products_by_category_id(category_id)
    else:
        products = Product.get_all_products()
    
    data = {'products': products, 'categories': categories}
    return render(request, 'index.html', data)
