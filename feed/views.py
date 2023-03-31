
import secrets
from django.shortcuts import render,redirect

from .models import Articles,Like,Announcements
from feed.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import   JsonResponse
from .forms import CommentForm,ArticleForm
from django.utils.text import slugify
from notification.signals import notification_signal
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Comments
from PIL import Image
from company.models import Company
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.views.decorators.cache import cache_page
from notification.models import Notification
# Create your views here.
@cache_page(60 * 5) # cache for 5 minutes
@login_required   
def add_article(request):
    if request.method=='POST':
            body=request.POST.get('body')
            author = request.POST.get('author')
            photo= request.FILES.get('article_image')
            categorytype=request.POST.get('post-type')
            article_form = ArticleForm(request.POST or None, request.FILES or None)
            if article_form.is_valid():
                #print(article_form.tag)
                obj=article_form.save(commit=False)
                if categorytype:
                    obj.category=categorytype
                obj.country= request.user.location
                if author == 'user':
                    user = request.user

                    obj.author = user
                else:
                     company = Company.objects.get(identifier = author)
                     obj.company = company  
                obj.body=f'<pre>{body}</pre>'
                if obj.title:
                     title = obj.title[:5]
                else:
                     title=''
                obj.slug = slug_generator(title=title,body=body[:5])
                if photo:
                     obj.article_image =image_commpress(photo)
                     obj.thumpnail = thumpnail(photo)
                obj.save()
                article_form.save_m2m()


                return redirect('articles')      
            else:
                article_form =ArticleForm()
                options = request.user.company_admin.all()
                return render (request, 'feed/add-article.html', {'form':article_form,'stylesheet':'styles/feed.css','options':options} )
    
    else:
        article_form =ArticleForm()
        options = request.user.company_admin.all()
        return render (request, 'feed/add-article.html',{'form':article_form,'stylesheet':'styles/feed.css','options':options} )

def slug_generator(title,body):
    if title:
        new_title = title
    else:
        new_title =" ".join(body.split(" "))
    random_string = secrets.token_hex(5)
    print(random_string)
    slug_string = " ".join([new_title, random_string])
    slug = slugify(slug_string)
    print(slug)
    return slug

@cache_page(60 * 5) # cache for 5 minutes
def articles (request):
    if request.user.is_authenticated:
        articles=Articles.objects.filter(status='Publish').order_by('-date')
        p=Paginator(articles,per_page=10)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 10
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).filter(num_times__gte=1).order_by('-num_times')[:top_n]
        options = request.user.company_admin.all()

        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags,
            'options':options
        }

        return render (request, 'feed/articles.html', context)
    
    else:
        context={
         
            'stylesheet':'styles/feed.css'
          }
        return render (request,'feed/home.html',context )

def article_details(request,article_slug):
    article=Articles.objects.get(slug=article_slug)
     #comment form
    comment_form = CommentForm()
    comments=article.comments.all().order_by('-date')[0:5]
    if request.user.is_authenticated:
        options = request.user.company_admin.all()
    else:
         options=None

    context={
        'article':article,
        'comment_form':comment_form,
        'comments':comments,
        'options':options
    }
    return render(request, 'feed/details.html',context)
@login_required   
def comment(request,article_slug):
                article=Articles.objects.get(slug=article_slug)
                comment = request.POST['comment']
                author= request.POST.get('author')
                article_author=article.author
                obj = Comments()
                obj.article = article
                if author == 'user':
                        obj.author = request.user
                        messagename=request.user.get_full_name()
                else:
                    companypage = Company.objects.get(identifier=author)
                    obj.companyauthor=companypage
                    messagename=companypage.name

                obj.comment = comment
                obj.article_id = article.id
                obj.save()
                message =f'{messagename} Commented on your post {article.body[5:30]}...'
                url ='/' + obj.article.slug

                if obj.author :
                            name=str(request.user.get_full_name())
                            img_url = obj.author.profilepic()
                            if article.author != request.user:
                                new_notification=Notification.objects.create(message=message,url=url,trigger=request.user)
                else:
                            name = str(messagename)
                            img_url= obj.companyauthor.logopic()
                            new_notification=Notification.objects.create(message=message,url=url,trigger_page=companypage)
                if new_notification:
                    article_author.usernotification.mynotification.add(new_notification)

                return JsonResponse({'comment':obj.comment,'name':name,'img':img_url})


@login_required   
def like_article(request, article_id):
        user=request.user
    
        article= Articles.objects.get(id=article_id)
        if user in article.likes.all():
            article.likes.remove(user)
            inliked = False
        else:
            article.likes.add(user)
            inliked = True
            message =f'{request.user.get_full_name()} liked your post {article.body[5:30]}...'
            if article.author:
                url ='/' + article.slug
                notification_signal.send(message =message,target=article.author,trigger=request.user,sender=None,url=url)

        like, created =Like.objects.get_or_create(user=user,article_id=article_id)
        if not created:
            if like.value=='Like':
                like.value=='Unlike'
            else:
                like.value ='Like'
        like.save()
          
        return JsonResponse({'likes': article.likes.count(),'userLike': inliked })




def search(request):
        query= request.POST.get('search-query')
        articles=Articles.objects.filter(body__icontains=query)
        p=Paginator(articles,per_page=5)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 5
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:top_n]
        
        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags,
            'query':query
        }

        return render (request, 'feed/articles.html', context)


def annoucement (request):
    if request.method== 'POST':
        user_profile =CustomUser.objects.all().filter( user_profile=request.user)[0]
        annoucement= request.POST.get('annoucement')
        annouce_type=request.POST.get('annouce_type')
        new_annoucment=Announcements()
        new_annoucment.annoucement=annoucement
        new_annoucment.annoucement_type=annouce_type
        new_annoucment.profile=user_profile
        new_annoucment.save()
        return redirect('annoucement' )   

    else:
        annoucements=Announcements.objects.all().order_by('-date')
        context={
        'annoucements':annoucements
        
    }
    return render(request, 'feed/annoucement.html',context)

@login_required   
def delete_article (request,slug):
        articleitem=Articles.objects.get(id=slug)
        articleitem.delete()
        return JsonResponse({'status': 'success'})   
def delete_annoucement (request,slug):

    if request.method=='POST':
        annoucemnt=Announcements.objects.all().filter(id=slug)[0]
        annoucemnt.delete()
        messages.success(request,'Announcement has been deleted')
        return redirect('annoucement')
    
@cache_page(60 * 5) # cache for 5 minutes
def filter_article(request,tag):
        filter_by = request.GET.get('filter_by')
        if filter_by == 'tag':
            articles = Articles.objects.filter(tag__slug=tag).filter(status='Publish').order_by('-date')
        if filter_by == 'category':
            articles = Articles.objects.filter(category=tag).filter(status='Publish').order_by('-date')

        p=Paginator(articles,per_page=10)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 10
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:top_n]
        
        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags,
            'pagefilter':filter_by

        }

        return render (request, 'feed/articles.html', context)


def image_commpress(image):

    img = Image.open(image)
    max_size = (1280, 720)
    img.thumbnail(max_size,Image.ANTIALIAS)
    output = io.BytesIO()
    img.save(output,format='png', quality=70)
    output.seek(0)
    compressed_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
    return compressed_image

def thumpnail(image):

    img = Image.open(image)
    max_size = (200, 200)
    img.thumbnail(max_size,Image.ANTIALIAS)
    output = io.BytesIO()
    img.save(output,format='png', quality=65)
    output.seek(0)
    compressed_image = InMemoryUploadedFile(output, 'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
    return compressed_image
