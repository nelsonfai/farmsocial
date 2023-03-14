from django.shortcuts import get_object_or_404, render,redirect
from.models import ProductItem
from .forms import ProductitemForm,ProductUpdate
from django.contrib import messages
from accounts.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from PIL import Image
from company.models import Company
from django.core.files.uploadedfile import InMemoryUploadedFile
import io
from django.views.decorators.cache import cache_page

# Create your views here.
@cache_page(60 * 5) # cache for 5 minutes
@login_required   
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
        mainimage= request.FILES.get('main_image')
        image2= request.FILES.get('image2')
        image3= request.FILES.get('image3')
        form.user_profile=request.user
        company = request.POST.get('company')
        print(form.user_profile)

        if form.is_valid:
            obj = form.save(commit=False)
            if company !='None':
                companypage = Company.objects.get(identifier=company)
                obj.companypage = companypage
            if mainimage:
                obj.main_image=thumpnail(mainimage)
                obj.thumpnail=thumpnailpic(mainimage)
            if image2:
                obj.image2=thumpnail(image2)
            if image3:
                obj.image3=thumpnail(image3)
            obj.save()
            messages.success(request,'Product added succesfully')
            return redirect ('market')
        else:
            options = request.user.company_admin.all()
            messages.success(request,'Product add failed Try again')
            form = ProductitemForm()
            context={
            "form":form,
            'options':options
              }
            return render (request,'marketplace/newproduct.html',context)
    else:
        profile=request.user
        initial_data={
                'user_profile':profile
            }
        form = ProductitemForm(initial=initial_data)
        options = request.user.company_admin.all()

        context={
            "form":form,
            'options':options
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
        productitems=ProductItem.objects.filter(product__contains=searched_product)
        p=Paginator(productitems,per_page=8)
        page=request.GET.get('page')
        paginated_product=p.get_page(page)
        context={
        "productitems": paginated_product
    }
    return render (request,'marketplace/market.html', context)

def filter (request):
    if request.method=='POST':
        category= request.POST.get('filter')
        print(category)
        productitems=ProductItem.objects.filter(product_category__contains=category)
        p=Paginator(productitems,per_page=8)
        page=request.GET.get('page')
        paginated_product=p.get_page(page)
        context={
        "productitems":paginated_product
    }
    return render (request,'marketplace/market.html', context)

@login_required(login_url='login')
def myproducts(request):
    profile=request.user
    productitems=ProductItem.objects.filter(user_profile=profile)
    p=Paginator(productitems,per_page=8)
    page=request.GET.get('page')
    paginated_product=p.get_page(page)
    context={
        "productitems":paginated_product
    }
    

    return render (request, 'marketplace/myproducts.html', context)


@login_required(login_url='login')
def edit_product (request,slug): 
    productitem=get_object_or_404(ProductItem,id=slug)

    if productitem.user_profile == request.user:

        if request.method == 'POST':
            form=ProductUpdate(request.POST or None, request.FILES or None, instance=productitem)
            mainimage= request.FILES.get('main_image')
            image2= request.FILES.get('image2')
            image3= request.FILES.get('image3')
            form.user_profile=request.user
            if form.is_valid():
                obj= form.save(commit=False)
                if mainimage:
                    obj.main_image=thumpnail(mainimage)
                if image2:
                    obj.image2=thumpnail(image2)
                if image3:
                    obj.image3=thumpnail(image3)
                obj.save()
                productitem = obj
                messages.success(request,'Product succesfully updated')
                

                return redirect ('myproducts' )  
        else:    
            form = ProductUpdate(instance=productitem)

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


def thumpnail(image):
    img = Image.open(image)
    max_size = (500, 500)
    img.thumbnail(max_size,Image.ANTIALIAS)
    output = io.BytesIO()
    img.save(output,format='png', quality=80)
    output.seek(0)
    compressed_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
    return compressed_image

def thumpnailpic(image):
    img = Image.open(image)
    max_size = (100, 100)
    img.thumbnail(max_size,Image.ANTIALIAS)
    output = io.BytesIO()
    img.save(output,format='png', quality=80)
    output.seek(0)
    compressed_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
    return compressed_image