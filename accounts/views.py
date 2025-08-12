from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import RegisterForm,LoginForm,changePassword,ProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login,logout

# Create your views here.
def register(request):
    form = RegisterForm()
    if request.user.is_authenticated:
        messages.warning(request, "You are already registered")
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            new_user=form.save()
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password1"]
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            messages.success(request, "You have successfully registered")
            return redirect('home')

    return render(request, 'register.html',{'form':form})

def userlogin(request):
    get_next=request.GET.get('next')
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in")
        return redirect('home')
    if request.POST: #لو الشخص دخل بيانات ودغط علي السبمت
        form = LoginForm(request.POST)
        if form.is_valid():
            # username=form.cleaned_data["username"]
            # password=form.cleaned_data["password"]
            # new_user = authenticate(username=username, password=password)
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request, "You have successfully logged in")
                return redirect('home')
            else:
                messages.error(request, "Invalid credentials")
    else:
        form = LoginForm() #لو اليوزر مسجلش بيانات اصلا هيديله الفورم


    return render(request, 'login.html',{'form':form,'next':get_next})

def user_logout(request):
    logout(request)
    # messages.success(request, "You have successfully logged out")
    return redirect('home')

def change_password(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You are not logged in")
        return redirect('login')
    if request.POST:
        form=changePassword(request.user,request.POST)
        if form.is_valid():
            user=form.save()

            login(request,user)
            messages.success(request, "Your password has been successfully changed")
            return redirect('home')
    else:
        form=changePassword(request.user)
    return render(request, 'change_password.html', {'form': form})    

def user_profile(request,pk):
    profile=Profile.objects.get(id=pk)
    if request.POST:
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.errors:
            messages.error(request, f'{form.errors}')
        if form.is_valid():
            new=form.save(commit=False)
            new.user=request.user
            new.save()
            messages.success(request, "Profile has been updated successfully")
            return redirect('profile', pk=profile.id)
    else:
        form=ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form, 'profile': profile})

