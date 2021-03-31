from django.shortcuts import render,HttpResponseRedirect
from django.contrib.auth.models import User
from .models import *
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

def home(request):
    if(request.method=="POST"):
        msg=request.POST.get('message')
        p=Product.objects.filter(Q(name__icontains=msg))
    else:
        p=Product.objects.all()
    return render(request,"index.html",{"Product":p})

@login_required(login_url='/login/')
def cartDetails(request):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect("/admin/")
    try:
        Seller.objects.get(uname=request.user)
        return  HttpResponseRedirect('/profile/')
    except:
        b=Buyer.objects.get(uname=request.user)
        cart=Cart.objects.filter(buyer=b)
        subtotal=0
        for i in cart:
            subtotal+=i.total
        if(subtotal<1000):
            delivery=150
        else:
            delivery=0
        finalAmount=subtotal+delivery
        return render(request,"cart.html",{"Cart":cart,"Sub":subtotal,"Delivery":delivery,"Final":finalAmount})

@login_required(login_url='/login/')
def deleteCart(request,num):
    cart=Cart.objects.get(id=num)
    cart.delete()
    return HttpResponseRedirect('/cart/')

@login_required(login_url='/login/')
def checkoutDetails(request):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin')
    try:
        user=Seller.objects.get(uname=request.user)
        return HttpResponseRedirect('/profile/')
    except:
        user=Buyer.objects.get(uname=request.user)
        if(request.method=="POST"):
            ch=Checkout()
            ch.user=user
            ch.address1=request.POST.get('address1')
            ch.address2=request.POST.get('address2')
            ch.pin=request.POST.get('pin')
            ch.city=request.POST.get('city')
            ch.state=request.POST.get('state')
            ch.name=request.POST.get('name')
            ch.phone=request.POST.get('phone')
            ch.email=request.POST.get('email')
            cart=Cart.objects.filter(buyer=user)
            ch.cart=cart[0]
            ch.total=cart[0].total
            ch.mode=request.POST.get('option')
            ch.notes=request.POST.get('message')
            ch.save()
            return HttpResponseRedirect('/confirm/')
        return render(request,"checkout.html",{"user":user})



def contactDetails(request):
    if(request.method=="POST"):
        c=Contact()
        c.name=request.POST.get('name')
        c.email=request.POST.get('email')
        c.subject=request.POST.get('subject')
        c.msg=request.POST.get('message')
        c.save()
        messages.success(request,"Message Sent")
        return HttpResponseRedirect('/contact/')
    return render(request,"contact-us.html")

def loginDetails(request):
    if(request.method=="POST"):
       uname=request.POST.get('uname')
       pword=request.POST.get('password')
       user=auth.authenticate(username=uname,password=pword)
       if(user is not None):
           auth.login(request,user)
           return HttpResponseRedirect('/profile/')
       else:
           messages.error(request,"Invalid User Name or Password")
    return render(request,"login.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def productDetails(request,num):
    p=Product.objects.get(id=num)
    if(request.method=="POST"):
        try:
            c=Cart()
            b=Buyer.objects.get(uname=request.user)
            c.product=p
            c.buyer=b
            c.quantity=int(request.POST.get('q'))
            c.color=request.POST.get('color')
            c.size=request.POST.get('size')
            c.total=c.product.finalPrice*c.quantity
            c.save()
            return HttpResponseRedirect('/cart/')
        except:
            return HttpResponseRedirect('/login/')
    return render(request,"product-details.html",{"Product":p,})

def shopDetails(request,cat,br):
    c=Category.objects.all()
    brand=Brand.objects.all()
    if(cat=="default" and br=="default"):
       p=Product.objects.all()
    elif(not cat=="default" and br=="default"):
        cobj=Category.objects.get(name=cat)
        p=Product.objects.filter(category=cobj)
    elif(cat=="default" and (not br=="default")):
        bobj=Brand.objects.get(name=cat)
        p=Product.objects.filter(brand=bobj)
    else:
        cobj=Category.objects.get(name=cat)
        bobj=Brand.objects.get(name=br)
        p=Product.objects.filter(brand=bobj,category=cobj)

    return render(request,"shop.html",{"Category":c,"Brand":brand,"Product":p,"Cat":cat,"Br":br})

def signupUser(request):
    choice=request.POST.get('option')
    if(choice=="seller"):
       s=Seller()
       s.name=request.POST.get('name')
       s.uname = request.POST.get('username')
       s.email = request.POST.get('email')
       pword = request.POST.get('password')
       try:
         user=User.objects.create_user(username=s.name,
                                     email=s.email,
                                     password=pword)
         s.save()
         messages.success(request,"Account Created !! please login ")
         return HttpResponseRedirect('/login/')
       except:
          messages.error(request,"User Name Already Taken")
          return render(request,"login.html")
    else:
        b=Buyer()
        b.name=request.POST.get('name')
        b.uname=request.POST.get('username')
        b.email=request.POST.get('email')
        pword=request.POST.get('password')
        try:
         user=User.objects.create_user(username=b.uname,email=b.email,password=pword)
         b.save()
         messages.success(request,"Account Created!! please login ")
         return HttpResponseRedirect('/login/')
        except:
         messages.error(request, "User Name Already Taken")
         return render(request, "login.html")



@login_required(login_url='/login/')
def profile(request):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    else:
        try:
            s=Seller.objects.get(uname=request.user)
            products=Product.objects.filter(seller=s)
            if(request.method=='POST'):
                s.name=request.POST.get('name')
                s.email = request.POST.get('email')
                s.phone = request.POST.get('phone')
                s.bankName = request.POST.get('bank')
                s.ifscCode = request.POST.get('ifsc')
                s.accountNumber = request.POST.get('account')
                s.save()
                return HttpResponseRedirect('/profile/')
            return render(request,"seller.html",{"User":s,"Product":products})
        except:
            b=Buyer.objects.get(uname=request.user)
            if (request.method == 'POST'):
                b.name = request.POST.get('name')
                b.email = request.POST.get('email')
                b.phone = request.POST.get('phone')
                b.address1 = request.POST.get('address1')
                b.address2 = request.POST.get('address2')
                b.city = request.POST.get('city')
                b.state = request.POST.get('state')
                b.pin = request.POST.get('pin')
                b.save()
                return HttpResponseRedirect('/profile/')
            return render(request,"buyer.html",{"User":b})


@login_required(login_url='/login/')
def addProduct(request):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('admin/')
    brand = Brand.objects.all()
    category = Category.objects.all()
    if (request.method == 'POST'):

       try:
          s=Seller.objects.get(uname=request.user)
          p=Product()
          p.name=request.POST.get('name')
          p.desc = request.POST.get('description')
          p.basePrice = int(request.POST.get('baseprice'))
          p.discount = request.POST.get('discount')
          p.finalPrice=p.basePrice-p.basePrice*int(p.discount)//100
          p.category=Category.objects.get(name=request.POST.get('category'))
          p.brand=Brand.objects.get(name=request.POST.get('brand'))
          if (request.POST.get('stock') == "2"):
              p.stock = True
          if (request.POST.get('red') == "2"):
              p.red = True
          if (request.POST.get('green')=="2"):
              p.green = True
          if (request.POST.get('black') == "2"):
              p.black =True
          if (request.POST.get('x') == "2"):
              p.x = True
          if (request.POST.get('m') == "2"):
              p.m = True
          if (request.POST.get('l') == "2"):
              p.l = True
          if (request.POST.get('xl') == "2"):
              p.xl =True
          p.img1 =request.FILES.get('img1')
          p.img2 =request.FILES.get('img2')
          p.img3 =request.FILES.get('img3')
          p.img4 =request.FILES.get('img4')
          p.img5 =request.FILES.get('img5')
          p.seller=s
          p.save()
          return HttpResponseRedirect('/profile/')
       except:
           return HttpResponseRedirect('/')

    return render(request,"addproduct.html",{"Brand":brand,"Category":category})

@login_required(login_url='/login/')
def deleteProduct(request,num):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    p=Product.objects.get(id=num)
    p.delete()
    return HttpResponseRedirect('/profile/')

@login_required(login_url='/login/')
def editProduct(request,num):
    user=User.objects.get(username=request.user)
    if(user.is_superuser):
        return HttpResponseRedirect('/admin/')
    p=Product.objects.get(id=num)
    category=Category.objects.all()
    brand=Brand.objects.all()
    if(request.method=='POST'):
        s = Seller.objects.get(uname=request.user)

        p.name = request.POST.get('name')
        if(not request.POST.get('description')==""):
            p.desc = request.POST.get('description')
        p.basePrice = int(request.POST.get('baseprice'))
        p.discount = request.POST.get('discount')
        p.finalPrice = p.basePrice - p.basePrice * int(p.discount) // 100
        p.category = Category.objects.get(name=request.POST.get('category'))
        p.brand = Brand.objects.get(name=request.POST.get('brand'))
        if (request.POST.get('stock') == "2"):
            p.stock = True
        if (request.POST.get('stock') == "1"):
            p.stock = False
        if (request.POST.get('red') == "2"):
            p.red = True
        if (request.POST.get('red') == "1"):
            p.red = False
        if (request.POST.get('green') == "2"):
            p.green = True
        if (request.POST.get('green') == "1"):
            p.green = False
        if (request.POST.get('black') == "2"):
            p.black = True
        if (request.POST.get('black') == "1"):
            p.black = False
        if (request.POST.get('x') == "2"):
            p.x = True
        if (request.POST.get('x') == "1"):
            p.x = False
        if (request.POST.get('m') == "2"):
            p.m = True
        if (request.POST.get('m') == "1"):
            p.m = False
        if (request.POST.get('l') == "2"):
            p.l = True
        if (request.POST.get('l') == "1"):
            p.l = False
        if (request.POST.get('xl') == "2"):
            p.xl = True
        if (request.POST.get('xl') == "1"):
            p.xl = False
        if(not request.FILES.get('img1')==None):
            p.img1 = request.FILES.get('img1')
        if (not request.FILES.get('img2') == None):
            p.img2 = request.FILES.get('img2')
        if (not request.FILES.get('img3') == None):
            p.img3 = request.FILES.get('img3')
        if (not request.FILES.get('img4') == None):
            p.img4 = request.FILES.get('img4')
        if (not request.FILES.get('img5') == None):
            p.img5 = request.FILES.get('img5')
        p.seller = s
        p.save()
        return  HttpResponseRedirect('/profile/')
    return render(request,"editproduct.html",{"Product":p,"Category":category,"Brand":brand})

def confirm(request):
    return render(request,"confirm.html")

@login_required(login_url='/login/')
def wishlistDetails(request,num):
    user = User.objects.get(username=request.user)
    if (user.is_superuser):
        return HttpResponseRedirect('/admin')
    try:
        user = Seller.objects.get(uname=request.user)
        return HttpResponseRedirect('/profile/')
    except:
        user=Buyer.objects.get(uname=request.user)
        w=Wishlist()
        product=Product.objects.get(id=num)
        w.user=user
        w.product=product
        w.save()
        return HttpResponseRedirect('/profile/')

@login_required(login_url='/login/')
def wishlistBuyer(request):
    user = User.objects.get(username=request.user)
    if (user.is_superuser):
        return HttpResponseRedirect('/admin')
    try:
        user = Seller.objects.get(uname=request.user)
        return HttpResponseRedirect('/profile/')
    except:
        user = Buyer.objects.get(uname=request.user)
        wish=Wishlist.objects.filter(user=user)
        return render(request,"wishlist.html",{"Wish":wish})

@login_required(login_url='/login/')
def wishlistDelete(request,num):
    wish=Wishlist.objects.get(id=num)
    wish.delete()
    return HttpResponseRedirect('/wishlist/')

