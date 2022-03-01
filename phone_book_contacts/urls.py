from django.urls import path
from .views import (
    ContactListView,
    creat_contact,
    delete_list_contact_view,
    delete_content_view,
    SearchContactListView,
    ContactDetailView,
    add_contact_by_file_view,
)

app_name = 'phone_book_contacts'

urlpatterns = [
    path('', ContactListView.as_view(), name='show_contact'),
    path('contact_<id>', ContactDetailView.as_view(), name='show_detail_contact'),
    path('create', creat_contact, name='creat_new_contact'),
    path('delete-list', delete_list_contact_view, name='delete_list_contact'),
    path('delete', delete_content_view, name='delete_contact'),
    path('search', SearchContactListView.as_view(), name='search_contact'),
    path('add_file', add_contact_by_file_view, name='add_contacts_by_file'),
]
