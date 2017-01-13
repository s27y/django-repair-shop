from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm

from .forms import ProfileForm, UserCreateForm , UserForm,MyAuthenticationForm

from .models import Profile


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        next_page = request.POST.get('next', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome %s. Thanks for logging in.' % username)
            if next_page != '':
                # Redirect to a previsou page.
                return HttpResponseRedirect(next_page)
            else:
                # Redirect to a default page.
                return HttpResponseRedirect(reverse('repairs:index'))
        else:
            if next_page:
                # Return an 'invalid login' error message.
                messages.error(request, 'Sorry, that login was invalid. Please try again.') 
                print '#########error'
                form = MyAuthenticationForm()
                if next_page:
                    return HttpResponseRedirect(next_page)
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'Sorry, that login was invalid. Please try again.') 
                form = MyAuthenticationForm()
                return render(request, 'accounts/login.html', { 'form': form })
            
    else: # GET
        form = MyAuthenticationForm()
        if request.user.is_authenticated:
                return HttpResponseRedirect(reverse('repairs:index'))
        else:
            return render(request, 'accounts/login.html', {
            'form': form, 
            'next': request.GET.get('next', '')
            })

def logout_view(request):
    #TODO
    logout(request)
    messages.success(request, ('You are now logged out.'))
    # Redirect to login page.
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def profile_view(request):
    return render(request, 'accounts/index.html')
    
    
@login_required
@transaction.atomic
def profile_update(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('accounts:profile_update')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile,initial={"company_name": request.user.profile.company_name})
        
        print '#### %s' % request.user.profile
    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def password_change(request):
    #TODO
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password updates success!')
            return HttpResponseRedirect(reverse('repairs:index'))
    else:
        form = PasswordChangeForm(user=request.user)
        return render(request, 'accounts/password_change.html', {'form': form})

def password_reset(request):
    #TODO
    form = PasswordResetForm()
    if request.method == 'POST':
        messages.error(request, 'Please contact admin')
        return render(request, 'accounts/password_reset.html', {'form': form})
    else:
        return render(request, 'accounts/password_reset.html', {'form': form})

@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.refresh_from_db() # This will load the Profile created by the Signal
            profile_form = ProfileForm(request.POST, instance=user.profile) # Reload the profile form with the profile instance
            profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            profile_form.save() # Gracefully save the form
            new_user = authenticate(username=user_form.cleaned_data['username'],
                                    password=user_form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            messages.success(request, ('Your account was successfully created!'))
            return HttpResponseRedirect(reverse('accounts:profile_update'))
        else:
            messages.error(request, ('Please correct the error below.'))
            return render(request, 'accounts/signup.html', {'user_form': user_form,'profile_form':profile_form})
    else: # GET
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('repairs:index'))
        else:
            user_form = UserCreateForm()
            profile_form = ProfileForm()
            return render(request, 'accounts/signup.html', {'user_form': user_form,'profile_form':profile_form})


def signin_view(request):
    user_form = UserCreateForm()
    profile_form = ProfileForm()
    login_form = AuthenticationForm()
    return render(request, 'accounts/signin.html', {
        'user_form': user_form,
        'profile_form':profile_form,
        'login_form': login_form,
        'next': request.GET.get('next', '')
        })

def hello(request):
    return HttpResponse('Hello World!')

def home(request):
    return render(request,'accounts/test.html', {'variable': 'world'})
