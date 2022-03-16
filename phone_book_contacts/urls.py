from django.urls import path
from .views import (
    ContactListView,
    creat_contact,
    delete_list_contact_view,
    delete_content_view,
    SearchContactListView,
    ContactDetailView,
    add_contact_by_file_view,
    update_contact_view,
    update_contact_publication,
)
from django.views.decorators.cache import cache_page

app_name = 'phone_book_contacts'

urlpatterns = [
    path('<user>', ContactListView.as_view(), name='show_contact'),
    path('<user>/contact_<id>', ContactDetailView.as_view(), name='show_detail_contact'),
    path('<user>/create', creat_contact, name='creat_new_contact'),
    path('<user>/delete-list', delete_list_contact_view, name='delete_list_contact'),
    path('<user>/delete', delete_content_view, name='delete_contact'),
    path('<user>/search', SearchContactListView.as_view(), name='search_contact'),
    path('<user>/add_file', add_contact_by_file_view, name='add_contacts_by_file'),
    path('<user>/update/contact_<id>', update_contact_view, name='update_contact'),
    path('<user>/update_contact_publication', update_contact_publication, name='update_contact_publication'),
]
