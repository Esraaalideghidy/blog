from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # path('',views.home,name='home')
    path('',home,name='home'),
    path('details/<int:pk>',detailed_blog,name='detailed_blog'),
    path('edit_blog/<int:pk>',edit_blog,name='edit_blog'),
    path('delete_blog/<int:pk>',delete_blog,name='delete_blog'),
    path('add_blog/',add_blog,name='add_blog'),
    path('tags/<slug:tag_slug>',get_tags,name='get_tags'),
    path('comment',save_comments,name='comment'),
    path('delete_comment',delete,name='delete_comment'),
    path('about',about,name='about'),
    path('contact',contact,name='contact'),
]

