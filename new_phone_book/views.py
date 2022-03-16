from django.shortcuts import redirect, reverse


def first_view(request):
    return redirect(reverse('phone_book_accounts:login'))
