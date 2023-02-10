from django.shortcuts import get_object_or_404, render,redirect
from.models import ProductItem
from .forms import ProductitemForm,ProductUpdate
from django.contrib import messages
from account.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your view
def market (request):
    productitems=ProductItem.objects.all()
    p=Paginator(productitems,per_page=8)
    page=request.GET.get('page')
    paginated_product=p.get_page(page)
    context={
        "productitems":paginated_product
    }
    

    return render (request,'marketplace/market.html', context)

@login_required(login_url='login')
   
def add_product (request):
    if request.method =='POST':
        profile=request.user
        initial_data={
            'user_profile':profile
        }
        form = ProductitemForm(request.POST, request.FILES)
        form.user_profile=request.user
        print(form.user_profile)

        if form.is_valid:
            
            form.save()
            messages.success(request,'Product added succesfully')
            return redirect ('market')
        else:
            messages.success(request,'Product add failed Try again')
            form = ProductitemForm()
            context={
            "form":form
              }
            return render (request,'marketplace/newproduct.html',context)

    profile=request.user
    initial_data={
            'user_profile':profile
        }
    form = ProductitemForm(initial=initial_data)
    context={
        "form":form
    }
    return render (request,'marketplace/newproduct.html',context)

def product (request,slug):
    productitem=ProductItem.objects.get(id=slug)
    productitem.view_count+=1
    productitem.save()

    context={
        "productitem":productitem
    }
    
    return render (request,'marketplace/product.html',context)

def search (request):
    if request.method=='POST':
        searched_product = request.POST.get('search')
        print(searched_product)
        productitems=ProductItem.objects.get(product__contains=searched_product)
        context={
        "productitems":productitems
    }
    return render (request,'marketplace/market.html', context)

def filter (request):
    if request.method=='POST':
        category= request.POST.get('filter')
        print(category)
        productitems=ProductItem.objects.filter(product_category__contains=category)
        context={
        "productitems":productitems
    }
    return render (request,'marketplace/market.html', context)

@login_required(login_url='login')
def myproducts(request):
    profile=CustomUser.objects.get(user_profile=request.user)
    productitems=ProductItem.objects.filter(user_profile=profile)

    context={
        "productitems":productitems
    }

    return render (request, 'marketplace/myproducts.html', context)


@login_required(login_url='login')
def edit_product (request,slug): 
    productitem=get_object_or_404(ProductItem,id=slug)

    if productitem.user_profile.user_profile == request.user:

        if request.method == 'POST':
            form=ProductUpdate(request.POST or None, request.FILES or None, instance=productitem)
            if form.is_valid():
                obj= form.save(commit=False)
                obj.save()
                productitem = obj
                messages.success(request,'Product succesfully updated')
                return redirect ('myproducts' ) 

        else:    
            form = ProductUpdate(

            initial= {
                'product':productitem.product,
                'product_description':productitem.product_description,
                'quantity':productitem.quantity,
                'price':productitem.price,
                'location':productitem.location,
                'product_category':productitem.product_category,
                'main_image':productitem.main_image,
                'image2':productitem.image2,
                'image3':productitem.image3,


            }
        )

        
            context={
                "form":form,
                'productitem':productitem
            } 
            

            return render (request,'marketplace/edit_product.html',context)

    else:
        return redirect ('market')




@login_required(login_url='login')
def delete_product (request,slug):

    if request.method=='POST':
        productitem=ProductItem.objects.get(id=slug)
        productitem.delete()
        messages.success(request,'Product has been deleted')
        return redirect('myproducts')
    else:
        return redirect('myproducts')

