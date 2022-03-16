from django.shortcuts import render, redirect, reverse
from .forms import LoginForm, RegisterForm, UpdateUserForm
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.cache import cache_page
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import Http404, HttpResponse

User = get_user_model()


# Create your views here.

def update_user_view(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            update_user_form = UpdateUserForm(request.POST or None, request.FILES or None)
            context = {
                'update_user_form': update_user_form
            }
            if update_user_form.is_valid():
                update_user_form.save(request.user.id)
                return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))
            return render(request, template_name='account/update_user.html', context=context)
        else:
            return HttpResponse('شما مجاز به این عمل نیستیند')
    return redirect(reverse('phone_book_accounts:login'))


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))
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
                return redirect(reverse('phone_book_contacts:show_contact', args=([user_name])))
        else:
            form.add_error('password', 'رمز یا نام کاربری نادرست است ')

    return render(request, template_name='account/login.html', context=context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))
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
            return redirect(reverse('phone_book_accounts:login'))
        else:
            form.add_error('user_name', "این کاربر با این نام کاربری وجود دارد")

    return render(request, 'account/register.html', context=context)


def logout_view(request):
    logout(request)
    return redirect(reverse('phone_book_accounts:login'))


class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'account/accounts.html'
    login_url = 'phone_book_accounts:login'
    paginate_by = 25

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(*args, object_list=object_list, **kwargs)
        context['user'] = self.request.user
        context['search_by'] = self.request.GET.get('search_by')
        page_nums = [1]
        current_page = context['page_obj'].number
        if context['page_obj'].has_previous() and current_page >= 3:
            page_nums.append(context['page_obj'].previous_page_number())
        if current_page != 1:
            page_nums.append(current_page)
        if context['page_obj'].has_next() and context['page_obj'].paginator.num_pages - 1 > current_page:
            page_nums.append(context['page_obj'].next_page_number())
        if page_nums.count(context['page_obj'].paginator.num_pages) == 0:
            page_nums.append(context['page_obj'].paginator.num_pages)
        context['page_nums'] = page_nums
        return context

    def get_queryset(self, *args, **kwargs):
        search_by = self.request.GET.get('search_by') or ''
        user_qu = User.objects.filter(username__icontains=search_by).exclude(username=self.request.user)
        return user_qu

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Http404 as e:
            page = int(self.request.GET.get('page') or 0)
            if page > 1:
                return redirect(self.request.META.get("HTTP_REFERER").replace(f'page={page}', f'page={page - 1}'))
            raise e
