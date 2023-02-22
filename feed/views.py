
import secrets
from django.shortcuts import render,redirect

from .models import Articles,Like,Announcements
from feed.models import CustomUser
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import  HttpResponseRedirect, JsonResponse
from django.urls import reverse
from .forms import CommentForm,ArticleForm
from django.utils.text import slugify
from notification.signals import notification_signal
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from .models import Comments
from PIL import Image

# Create your views here.
@login_required   
def add_article(request):
    if request.method=='POST':
            body=request.POST.get('body')
            article_form = ArticleForm(request.POST or None, request.FILES or None)
            if article_form.is_valid():
                obj=article_form.save(commit=False)
                obj.author = request.user
                obj.article_image = image_commpress(obj.article_image)
                obj.thumpnail= thumpnail(obj.article_image)
                
                obj.body=f'<pre>{body}</pre>'
                obj.slug = slug_generator(title=obj.title[:5],body=body[:5])
                
                obj.save()
                return redirect('articles')      
            else:
                article_form =ArticleForm()
                return render (request, 'feed/add-article.html', {'form':article_form,'stylesheet':'styles/feed.css'} )
    
    else:
        article_form =ArticleForm()

        return render (request, 'feed/add-article.html',{'form':article_form,'stylesheet':'styles/feed.css'} )

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

def articles (request):
    if request.user.is_authenticated:
        articles=Articles.objects.all().order_by('-date')
        p=Paginator(articles,per_page=3)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 10
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:top_n]
        
        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags
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

    context={
        'article':article,
        'comment_form':comment_form,
        'comments':comments,
        
    }
    return render(request, 'feed/details.html',context)
@login_required   
def comment(request,article_slug):
                article=Articles.objects.get(slug=article_slug)
                comment = request.POST['comment']
                obj = Comments()
                obj.article = article
                obj.author = request.user
                obj.comment = comment
                obj.article_id = article.id
                obj.save()
                message =f'{request.user.get_full_name()} Commented on your post {article.body[5:30]}...'
                notification_signal.send(message =message,target=article.author,trigger=request.user,sender=None)

                return JsonResponse({'success':'succes' })


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
            notification_signal.send(message =message,target=article.author,trigger=request.user,sender=None)

        like, created =Like.objects.get_or_create(user=user,article_id=article_id)
        if not created:
            if like.value=='Like':
                like.value=='Unlike'
            else:
                like.value ='Like'
        like.save()
          
        return JsonResponse({'likes': article.likes.count(),'userLike': inliked })




def search(request,slug):
        articles=Articles.objects.filter(body__icontains=slug)
        p=Paginator(articles,per_page=5)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 5
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:top_n]
        
        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags,
            'query':slug
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
        messages.success(request,'Article has been deleted')
        return JsonResponse({'status': 'success'})   
def delete_annoucement (request,slug):

    if request.method=='POST':
        annoucemnt=Announcements.objects.all().filter(id=slug)[0]
        annoucemnt.delete()
        messages.success(request,'Announcement has been deleted')
        return redirect('annoucement')
def filter_article(request,tag):
        articles = Articles.objects.filter(tag__name=tag)
        p=Paginator(articles,per_page=3)
        page=request.GET.get('page')
        paginated_article=p.get_page(page)
        top_n = 10
        most_used_tags = Tag.objects.annotate(num_times=Count('taggit_taggeditem_items')).order_by('-num_times')[:top_n]
        
        context={
            'articles':paginated_article,
            'stylesheet':'styles/feed.css',
            'tags':most_used_tags
        }

        return render (request, 'feed/articles.html', context)


def image_commpress(image):
    img = Image.open(image)
    # Resize the image to a maximum width of 1000 pixels
    if img.width > 1000:
        img.thumbnail((1000, 1000))
    # Save the image in JPEG format with 70% quality
    img.save("optimized.jpg", "JPEG", quality=70,exif="")
    return img

def thumpnail(image):
    img = Image.open(image)
    # Resize the image to a maximum width of 1000 pixels
    if img.width > 200:
        img.thumbnail((200, 200))
    # Save the image in JPEG format with 70% quality
    img.save("optimized.jpg", "JPEG", quality=70,exif="")
    return img
