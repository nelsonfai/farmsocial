from django.urls import path
from . import views



urlpatterns = [
    
    path('',views.articles, name='articles'),
    path('<slug:article_slug>', views.article_details, name="details"),
    path('<slug:article_id>/like',views.like_article, name='like_article'),
    path('filter/<slug:tag>',views.filter_article, name='filter'),
    path('add-article/',views.add_article, name='add_article'),
    path('<slug:article_slug>/comment',views.comment, name='comment'),
   
    path('annoucement/',views.annoucement, name='annoucement'),
     path('delete_article/<slug:slug>',views.delete_article , name='delete_article'),
    path('delete_annoucement/<slug:slug>',views.delete_annoucement , name='delete_annoucement'),
  
  
]
