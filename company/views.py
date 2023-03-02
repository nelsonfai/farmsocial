from django.shortcuts import redirect, render
from company.models import Company
from django.http import  HttpResponseRedirect, JsonResponse
from company.forms import CompanyCreationForm,DashboardForm
# Create your views here.

def create_company(request):
    if request.method == 'POST':
        form = CompanyCreationForm(request.POST or None,)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect('dashboard', obj.identifier)
        else:
            form = CompanyCreationForm()
            context={
                'form':form
            }
            return render(request, 'company/create-company.html',context)
    else:
            form = CompanyCreationForm()
            context={
                'form':form
            }
            return render(request, 'company/create-company.html',context)


def dashboard(request,identifier):
    company= Company.objects.get(identifier = identifier)
    if request.method == 'POST':
        form = DashboardForm(request.POST or None, request.FILES or None ,instance=company)
        if form.is_valid():
            form.save()
            return redirect('companyprofile', company.identifier, company.name)
        else:
            company= Company.objects.get(identifier = identifier)
            form = DashboardForm(instance=company)
            return render(request, 'company/dashboard.html',{'profile':form,'company':company})
    else:
            company= Company.objects.get(identifier = identifier)
            form = DashboardForm(instance=company)
            context= {'profile':form,'company':company}
            return render(request, 'company/dashboard.html', context)


def company_profile(request,slug,name):
   company = Company.objects.get(identifier = slug)
   products= company.companyproduct.all()
   companysuggestions = Company.objects.exclude(identifier=slug)
   return render(request,'company/companyprofile.html', {'profile':company,'products':products,'companysuggestions':companysuggestions})

def follow_page(request,slug):
   company = Company.objects.get(identifier=slug)
   if request.user in company.pagefollowers.all():
        company.pagefollowers.remove(request.user)
        return JsonResponse({'success':'follow' })
   else:
        company.pagefollowers.add(request.user)
        return JsonResponse({'success':'unfollow' })

