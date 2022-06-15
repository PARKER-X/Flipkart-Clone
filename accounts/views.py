from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from store.models import *
from .forms import LoginForm, UserChangeForm, ProfileEditForm

# Create your views here.
def user_login(request):
    if request.method=='POST':
        form  = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username= cd['username'], password = cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticate Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form':form})





def register(request):
    if request.method=='POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(user=new_user)
            return render(request,'accounts/register_done.html',{'new_user': new_user, 'new_user': new_user})
    else:
        user_form = UserCreationForm()
    return render(request,'accounts/register.html',{'user_form': user_form})



@login_required
def edit(request):
    if request.method=='POST':
        user_form =  UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data= request.POST, files = request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
        
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request,'accounts/edit.html',{'user_form': user_form,'profile_form': profile_form})