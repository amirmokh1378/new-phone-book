from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import os
from django.db.models import Q


# Create your models here.


# def contact_image_directory_path(instance, filename):
#     base_name, ext = os.path.splitext(filename)
#     return f'UserInFo/{instance}/{instance}{ext}'


class ContactManager(models.Manager):
    def search(self, user, name='', family='', email='', phone='', num_company_or_home='', address='',
               ):
        lookup = Q(name__icontains=name) & Q(family__icontains=family) & Q(email__icontains=email) & Q(
            phone__icontains=phone) & Q(num_company_or_home__icontains=num_company_or_home) & Q(
            address__icontains=address)
        return user.contact_set.filter(lookup).distinct()

    def get_max_id_or_1(self):
        id__max = self.aggregate(models.Max('id'))['id__max']
        if id__max is not None:
            id__max += 1
        return id__max or 1

    def search_by_or_name_phone_email_family(self, user, search_by=''):
        lookup = Q(name__icontains=search_by) | Q(family__icontains=search_by) | Q(email__icontains=search_by) | Q(
            phone__icontains=search_by)
        return user.contact_set.filter(lookup).distinct()


class Contact(models.Model):
    name = models.CharField(max_length=20)
    family = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=10, blank=True, default='')
    address = models.TextField(max_length=400, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = ContactManager()

    def __str__(self):
        return self.name


def set_name_and_folder_excel_file(instance, filename):
    baseName, extension = os.path.splitext(filename)
    return f'excel_file/{instance.user.username}{extension}'


class ContactFile(models.Model):
    file = models.FileField(upload_to=set_name_and_folder_excel_file)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def check_extension(self):
        name, extension = os.path.splitext(self.file.name)
        if extension == '.xlsx':
            return 'xlsx'
        if extension == '.csv':
            return 'csv'
        raise ValidationError('the file must be excel or csv')
