from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.cache import cache_page

User = get_user_model()


# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    context = {
        'login_form': form,
        'body': 'hold-transition login-page',
    }

    if form.is_valid():
        password = form.cleaned_data.get('password')
        user_name = request.POST['user_name']
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                return redirect(reverse('phone_book_contacts:show_contact'))
        else:
            form.add_error('password', 'رمز یا نام کاربری نادرست است ')

    return render(request, template_name='account/login.html', context=context)


def register_view(request):
    form = RegisterForm(request.POST or None)
    context = {
        'register_form': form,
        'body': 'hold-transition register-page'
    }

    if form.is_valid():
        user_name = form.cleaned_data['user_name']
        password = form.cleaned_data['password']
        email = request.POST['email']
        is_user_exist = User.objects.filter(username=user_name).exists()
        if not is_user_exist:
            user = User(username=user_name, email=email)
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect(reverse('phone_book_contacts:show_contact'))
        else:
            form.add_error('user_name', "این کاربر با این نام کاربری وجود دارد")

    return render(request, 'account/register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse('phone_book_accounts:login'))
