from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.views import View
from django.db.models import Q
from .models import Customer,Product,Cart,OrderPlaced
from .forms import CustomerProfileForm, CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# def home(request):
#  return render(request, 'app/home.html')

class ProductView(View):

 def get(self,request):
    topwears=Product.objects.filter(category="TW")
    bottomwears=Product.objects.filter(category="BW")
    mobiles=Product.objects.filter(category="M")
    return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears,'mobiles':mobiles})

# def product_detail(request):
#  return render(request, 'app/productdetail.html')

# class ProductDetailView(View):
#  def get(self,request,pk):
#   product=Product.objects.get(id=pk)
#   return render(request, 'app/productdetail.html', {'product':product})
  


class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        if request.user.is_authenticated:
            item_already_in_cart = False
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user= request.user)).exists()
            print(item_already_in_cart)
            cn = Cart.objects.filter(user=request.user).count()
            return render(request, 'app/Productdetail.html', {'product':product,'item_already_in_cart':item_already_in_cart, 'cn':cn})
        else:
            return render(request, 'app/Productdetail.html', {'product':product})

# def show_cart(request):
#   if request.user.is_authenticated:
#     user=request.user
#     cart=Cart.objects.filter(user=user)
#     return render(request, 'app/addtocart.html', {'carts':cart})

# def add_to_cart(request):
#  user=request.user
#  product_id=request.GET.get('prod_id')
#  product=Product.objects.get(id=product_id)
#  Cart(user=user,product=product).save()
#  return redirect('/cart')
@login_required
def add_to_cart(request):
    user = request.user
    cn = Cart.objects.filter(user=request.user).count()
    product_id = request.GET.get('prod_id')
    print("heilsd",product_id)
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart', {'cn':cn})
    
@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cn = Cart.objects.filter(user=request.user).count()
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==user]
        # print(cart_product)
        if cart_product:
            for p in cart_product:
                amount =(p.quantity * p.product.discount_price) + amount
            total_amount = amount + shipping_amount
            return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount , 'total_amount':total_amount, 'ship_amount':shipping_amount, 'cn':cn})
        else:
          return render(request,'app/emptycart.html')


def plus_cart(request):
  user = request.user
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    print(prod_id)
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount = 0.0
    shipping_amount = 70.0
  
    cart_product = [p for p in Cart.objects.all() if p.user ==user]
    # print(cart_product)
   
    for p in cart_product:
      amount =(p.quantity * p.product.discount_price) + amount
    data = {
         'quantity':c.quantity,
         'amount':amount,
         'total_amount':amount+ shipping_amount
     }
  return JsonResponse(data)


def minuse_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            amount =(p.quantity * p.product.selling_price) + amount
        data = {
            'quantity':c.quantity,
            'amount':amount,
            'total_amount':total_amount+ shipping_amount
        }
        return JsonResponse(data)
    
    

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        total_amount=0.0
        cart_product = [p for p in Cart.objects.all() if p.user ==request.user]
        for p in cart_product:
            amount =(p.quantity * p.product.selling_price) + amount
        data = {
            'amount':amount,
            'total_amount':total_amount+ shipping_amount
        }
        return JsonResponse(data)
 
def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request):
 return render(request, 'app/profile.html')

@login_required
def address(request):
 add=Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})
@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html',{'order_placed':op})

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request,data=None):

    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='apple' or data=='samsung' or data=='vivo':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=="Below":
        mobiles=Product.objects.filter(category='M').filter(discount_price__lt=50000)
    elif data=="Above":
        mobiles=Product.objects.filter(category='M').filter(discount_price__gt=50000)    
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def login(request):
 return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
  def get(self,request):
    form=CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html', {'form':form})

  def post(self,request):
    form=CustomerRegistrationForm(request.POST)
    if form.is_valid():
      messages.success(request,'Congratulations!! Registered successfully')
      form.save()
    return render(request, 'app/customerregistration.html', {'form':form})
  
def checkout(request):
    user = request.user 
    cn = Cart.objects.filter(user=request.user).count()
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    for x in cart_items:
      #  for y in x:
          print(x.total_cost)
    amount = 0.0
    shipping_amount = 70.0
    total_amount=0
    cart_product = [p for p in Cart.objects.all() if p.user ==user]
    if cart_product:
        for p in cart_product:
            amount =(p.quantity * p.product.discount_price) + amount
        total_amount = amount + shipping_amount
        return render(request, 'app/checkout.html', {'add':add, 'total_amount':total_amount, 'cn':cn, 'cart_items':cart_items})
    
@method_decorator(login_required ,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form=CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
  def post(self,request):
    form=CustomerProfileForm(request.POST)
    if form.is_valid():
      user = request.user
      name=form.cleaned_data['name']
      locality=form.cleaned_data['locality']
      city=form.cleaned_data['city']
      state=form.cleaned_data['state']
      zipcode=form.cleaned_data['zipcode']
      reg=Customer(user=user,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
      reg.save()
      messages.success(request,'congrations !! Profile Updated Successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
def payment_done(request):
    user = request.user  
    cn = Cart.objects.filter(user=request.user).count()
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    total_amount=0
    cart_product = [p for p in Cart.objects.all() if p.user ==user]
    if cart_product:
        for p in cart_product:
            amount =(p.quantity * p.product.selling_price) + amount
        total_amount = (amount + shipping_amount)
        total_payment= total_amount * 100
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
                OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
                c.delete()
        return render(request, 'app/payment.html', {'payment':total_amount, 'payment1': total_payment})
    return render(request, 'app/payment.html',)
        
    # return redirect("/payment/")
def success(request):
    return render(request, 'app/success.html',)
   