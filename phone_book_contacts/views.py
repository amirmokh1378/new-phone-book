from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Contact
from django.views.generic import ListView, DeleteView
from .forms import CreateContactForm, AddFileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import ContactFilter
from new_phone_book.settings import engine
from phone_book_tools.tools import *
import pandas as pd
from django.http import Http404, HttpResponse
from sqlalchemy.exc import IntegrityError, DataError
from django.contrib.auth import get_user_model
import numpy as np
User = get_user_model()


# Create your views here.


class ContactDetailView(DeleteView):
    model = Contact
    login_url = 'phone_book_contacts:login'
    template_name = 'contact/detail.html'

    def get_object(self, queryset=None):
        id = self.kwargs['id']
        obj = get_object_or_404(self.model, id=id, user=self.request.user)
        return obj


class SearchContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contact/search.html'
    login_url = 'phone_book_contacts:login'
    paginate_by = 25

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(SearchContactListView, self).get_context_data(*args, object_list=object_list, **kwargs)
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

        context[
            'search_by'] = '&name__icontains=' + f"{self.request.GET.get('name__icontains') or ''}" + '&tel_work__icontains=' + f"{self.request.GET.get('tel_work__icontains') or ''}" + '&phone__icontains=' + f"{self.request.GET.get('phone__icontains') or ''}" + '&tel_home__icontains=' + f"{self.request.GET.get('tel_home__icontains') or ''}" + '&comment__icontains=' + f"{self.request.GET.get('comment__icontains') or ''}" + '&is_public__icontains=' + f"{self.request.GET.get('is_public__icontains') or ''}"
        return context

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        contact_qu = user.contact_set.all()
        contact_filter = ContactFilter(self.request.GET, contact_qu)
        return contact_filter.qs

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Http404 as e:
            page = int(self.request.GET.get('page') or 0)
            if page > 1:
                return redirect(self.request.META.get("HTTP_REFERER").replace(f'page={page}', f'page={page - 1}'))
            raise e


class ContactListView(LoginRequiredMixin, ListView):
    model = Contact
    template_name = 'contact/main_contact.html'
    login_url = 'phone_book_accounts:login'
    paginate_by = 25

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super(ContactListView, self).get_context_data(*args, object_list=object_list, **kwargs)
        context['user'] = User.objects.filter(username=self.kwargs['user']).first()
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
        user = self.kwargs['user']
        if self.request.user.username == user:
            contact_qu = Contact.objects.search_by_or_name_phone_email_family(user=user,
                                                                              search_by=self.request.GET.get(
                                                                                  'search_by') or '')
        else:
            contact_qu = Contact.objects.search_by_or_name_phone_email_family_and_public(user=user,
                                                                                         search_by=self.request.GET.get(
                                                                                             'search_by') or '')
        return contact_qu

    def get(self, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except Http404 as e:
            page = int(self.request.GET.get('page') or 0)
            if page > 1:
                return redirect(self.request.META.get("HTTP_REFERER").replace(f'page={page}', f'page={page - 1}'))
            raise e


def creat_contact(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            create_contact_form = CreateContactForm(request.POST or None)
            context = {
                'create_contact_form': create_contact_form,
            }
            if create_contact_form.is_valid():
                create_contact_form.save(request.user, None)
                return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))

            return render(request, template_name='contact/create_contact.html', context=context)
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    return redirect(reverse('phone_book_accounts:login'))


def delete_list_contact_view(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            if request.method == 'POST':
                list_id = request.POST.getlist('id')
                Contact.objects.filter(user=request.user, pk__in=list_id).delete()
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    return redirect(reverse('phone_book_accounts:login'))


def delete_content_view(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            if request.method == 'POST':
                id = request.POST.get('id')
                Contact.objects.filter(user=request.user, id=id).delete()
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    return redirect(reverse('phone_book_accounts:login'))


def update_contact_view(request, user, id):
    if request.user.is_authenticated:
        if user == request.user.username:
            contact_object = Contact.objects.get(user__username=user, pk=int(id))
            create_contact_form = CreateContactForm(request.POST or None)
            context = {
                'contact_object': contact_object,
                'create_contact_form': create_contact_form,
                'user': user
            }
            if create_contact_form.is_valid():
                create_contact_form.save(request.user, id)
                return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))

            return render(request, template_name='contact/update_contact.html', context=context)
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    return redirect(reverse('phone_book_accounts:login'))


def update_contact_publication(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            if request.method == 'POST':
                yes_list_id = request.POST.getlist('yes')
                no_list_id = request.POST.getlist('no')
                Contact.objects.filter(user=request.user, pk__in=yes_list_id).update(is_public='??????')
                Contact.objects.filter(user=request.user, pk__in=no_list_id).update(is_public='??????')
            return redirect(request.META.get("HTTP_REFERER"))
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    return redirect(reverse('phone_book_accounts:login'))


def add_contact_by_file_view(request, user):
    if request.user.is_authenticated:
        if user == request.user.username:
            add_file_form = AddFileForm(request.POST or None, request.FILES or None)
            context = {
                'add_file_form': add_file_form,
                'body': 'hold-transition register-page'
            }
            if add_file_form.is_valid():
                try:
                    if is_extension_xlsx(str(add_file_form.cleaned_data.get('file'))):
                        df = pd.read_excel(add_file_form.files['file'])
                    elif is_extension_csv(str(add_file_form.cleaned_data.get('file'))):
                        df = pd.read_csv(add_file_form.files['file'])
                    else:
                        add_file_form.add_error('file', '???????? ???????? ???????? ???? ???? ???? ???? ????????')
                        return render(request, template_name='contact/add_contact_by_file.html', context=context)
                    # --------------

                    df = df.astype(str)
                    df = df.replace('nan', None)

                    # --------------
                    data_frame_key_list = df.keys()
                    # field_list = ['name', 'family', 'email', 'phone', 'address']
                    field_list = [field.name for field in Contact._meta.get_fields()]
                    field_list.pop(0)
                    field_list.pop()
                    field_list.pop()
                    data_frame_key_list, fields_not_in_data_frame_keys_list = get_equal_items_list_one_in_list_tow(
                        field_list, data_frame_key_list)
                    if len(fields_not_in_data_frame_keys_list) != 0:
                        add_file_form.add_error('file',
                                                f'?????? ?????????? {fields_not_in_data_frame_keys_list} ????  ???????? ???????? ??????????')
                        return render(request, template_name='contact/add_contact_by_file.html', context=context)
                    df = df[field_list]
                    df['user_id'] = request.user.id
                    df['is_public'] = request.POST.get('is_public')
                    df.index += Contact.objects.get_max_id_or_1()
                    df.to_sql(Contact._meta.db_table, con=engine, if_exists='append', index_label='id')
                    request.FILES['file'] = None
                    return redirect(reverse('phone_book_contacts:show_contact', args=([request.user.username])))
                except IntegrityError as e:
                    add_file_form.add_error('file', '???????? name ?????????? ???????? ????????')
                except DataError as e:
                    # {c: df[c].map(lambda x: len(str(x))).max() for c in df.columns}
                    column = 'name'
                    error_text = ''
                    con = 100
                    s = df[column].str.len().between(0, con)
                    cells = list(s[s == False].index)
                    if len(cells) != 0:
                        error_text += ' ?????? ???????? ???? ' + f'{cells}' + ' ???? ???????? ' + f'{column}' + ' ???????? ???????????? ???? ' + f'{con}' + ' ????????' + '\n'
                    column = 'phone'
                    con = 100
                    s = df[column].str.len().between(0, con)
                    cells = list(s[s == False].index)
                    if len(cells) != 0:
                        error_text += ' ?????? ???????? ???? ' + f'{cells}' + ' ???? ???????? ' + f'{column}' + ' ???????? ???????????? ???? ' + f'{con}' + ' ????????' + '\n'
                    column = 'tel_work'
                    con = 100
                    s = df[column].str.len().between(0, con)
                    cells = list(s[s == False].index)
                    if len(cells) != 0:
                        error_text += ' ?????? ???????? ???? ' + f'{cells}' + ' ???? ???????? ' + f'{column}' + ' ???????? ???????????? ???? ' + f'{con}' + ' ????????' + '\n'
                    column = 'tel_home'
                    con = 100
                    s = df[column].str.len().between(0, con)
                    cells = list(s[s == False].index)
                    if len(cells):
                        error_text += ' ?????? ???????? ???? ' + f'{cells}' + ' ???? ???????? ' + f'{column}' + ' ???????? ???????????? ???? ' + f'{con}' + ' ????????' + '\n'
                    column = 'comment'
                    con = 1000
                    s = df[column].str.len().between(0, con)
                    cells = list(s[s == False].index)
                    if len(cells) != 0:
                        error_text += ' ?????? ???????? ???? ' + f'{cells}' + ' ???? ???????? ' + f'{column}' + ' ???????? ???????????? ???? ' + f'{con}' + ' ????????' + '\n'

                    add_file_form.add_error('file', error_text)
                except:
                    add_file_form.add_error('file', '???????? ?????????? ?????? ???????? ???? ???????????????? ?????? ??????????')
            return render(request, template_name='contact/add_contact_by_file.html', context=context)
        else:
            return HttpResponse('?????? ???????? ???? ?????? ?????? ??????????????')
    else:
        return redirect(reverse('phone_book_accounts:login'))
