# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from .models import login,Signup
from django.contrib import messages
from django import template
from .models import Products, Cart
from django.http import JsonResponse
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


# Create your views here.

def homepage(request):
    return render(request, 'ecom.html')



def Loginpage(request):
    return render(request,"login.html")

def Signuppage(request):
    return render(request,"signup.html")

# sugnup deatils.......................................................
def Signupdetails(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        Signup(name=name, email=email, password=password).save()
        return redirect('login')
    return render(request, 'signup.html')
    

# login details.......................................................

def Logindetails(request):
    if request.method == 'POST':
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = Signup.objects.filter(name=username, password=password)
        if user:
            return redirect('collection')
        else:
            return render(request, 'login.html')

# collection...............................................................

def collection_view(request):
    # Fetch all products from the database
    products = Products.objects.all()
    
    # Pass the products to the template
    context = {
        'products': products
    }
    
    # Render the template with the context
    return render(request, 'ecom.html', context)



def product_detail(request, product_id):
    product = get_object_or_404(Products, id = product_id)
    return render(request, 'product_detail.html', {'product': product})

# search box...............................................................

def searchi(request):
    query = request.GET.get("search", '')
    if query:
        products = Products.objects.filter(name__icontains=query)
    else:
        products = Products.objects.all()
    
    return render(request, 'ecom.html', {'products': products, 'query': query})


# cart..................................................................




# View to display cart
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# Add to cart function
def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

# Update cart quantity
def update_cart(request, cart_id, action):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease" and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()
    return JsonResponse({"quantity": cart_item.quantity, "total_price": cart_item.total_price()})

# remove from cart
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return JsonResponse({"success": True})


# invoice...............................................................


# Function to generate PDF invoice

def generate_invoice_pdf(cart_items, total_price):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("CHRONOGRAPH.in Invoice", styles['Title']))

    data = [['Product', 'Quantity', 'Unit Price', 'Total']]
    for item in cart_items:
        data.append([item.product.name, item.quantity, f'${item.product.price}', f'${item.total_price()}'])

    data.append(['', '', 'Grand Total', f'${total_price}'])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)
    return response



# Checkout function
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price() for item in cart_items)
    
    if request.method == "POST":
        response = generate_invoice_pdf(cart_items, total_price)
        cart_items.delete()  # Empty cart after checkout
        return redirect('home')
        return response

    return render(request, 'checkout.html', {'total_price': total_price})
