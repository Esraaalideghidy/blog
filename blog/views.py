from django.shortcuts import redirect, render, get_object_or_404
from .models import Blog,Comment
from taggit.models import Tag 
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from accounts.models import Profile
# Create your views here.
@login_required
def home(request):
    search=request.GET.get('search')
    if search:
        blog_view=Blog.objects.filter(Q(title__icontains=search) & Q(content__icontains=search)).order_by('-id')
    else:
        blog_view=Blog.objects.all().order_by('-id')    
    page=request.GET.get('page',1)
    paginator=Paginator(blog_view, 2)
    try:
        posts=paginator.page(page)
    except PageNotAnInteger:
        posts=paginator.page(1) 
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request, 'index.html', {'blog_view': posts})

@login_required
def detailed_blog(request,pk):
    blog_detail=Blog.objects.get(id=pk)
    comments=Comment.objects.filter(blog=blog_detail)
    return render(request, 'details.html',{'blog_detail': blog_detail,'comments': comments})

@login_required
def get_tags(request,tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)  # يجلب التصنيف أو يعطي 404 إذا لم يكن موجودًا
    blogs = Blog.objects.filter(tags=tag).order_by('-id')
    page = request.GET.get('page', 1)
    paginator = Paginator(blogs, 2)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context={
        'blog_view': posts,
        'tag': tag,
    }    
    return render(request, 'tags.html', context)


def save_comments(request):
    if request.method=='POST':
        blog_id=request.POST.get('blog_id')
        comment_text=request.POST.get('comment_text')
        blog=Blog.objects.get(id=blog_id)
        user=request.user
        if comment_text:  
            new_comment=Comment.objects.create(content=comment_text,active=True,blog=blog,user=user)
            new_comment.save()
    return redirect('detailed_blog', blog_id)    
def delete(request):
    if request.method == 'POST':
        pk=request.POST.get('id_delete')
        id_blog=request.POST.get('id')
        comment=get_object_or_404(Comment, id=pk)
        comment.delete()
        return redirect('detailed_blog',id_blog)
    

@login_required
def edit_blog(request,pk):
    blog=Blog.objects.get(id=pk)
    if request.POST:
        form=EditBlog(request.POST,request.FILES,instance=blog)
        if form.errors:
            messages.error(request, f'{form.errors}')
        if form.is_valid():
            form.save()
            messages.success(request, "Blog has been updated successfully")
            return redirect('detailed_blog', blog.id)
    else:
        form=EditBlog(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})     

@login_required
def delete_blog(request,pk):
    blog=Blog.objects.get(id=pk)
    blog.delete()
    messages.success(request, "Blog has been deleted successfully")
    return redirect('home')
@login_required
def add_blog(request):
    if request.POST:
        form=AddBlog(request.POST, request.FILES)
        if form.errors:
            messages.error(request, f'{form.errors}')
        if form.is_valid():
            new=form.save(commit=False)
            new.author=request.user
            new.save()
            messages.success(request, "Blog has been created successfully")
            return redirect('home')
    else:
        form=AddBlog()
    return render(request, 'add_blog.html', {'form': form})
        


@login_required
def about(request) :
    profile=Profile.objects.all()
    about = About.objects.all().first()
    return render(request, 'about.html', {'about': about,'profile': profile})




def contact(request):
    contact = ContactInfo.objects.all().first()
    if request.POST:
        form=ContactForm(request.POST)
        if form.is_valid():
            new=form.save(commit=False)
            new.user=request.user
            new.save()
            messages.success(request, "Your message has been sent successfully")
            return redirect('home')
    else:
        form=ContactForm()    
    return render(request, 'contact.html',{'contact':contact,'form':form})