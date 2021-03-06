from django.core.exceptions import ValidationError
from django.db import models
import os
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.


# def contact_image_directory_path(instance, filename):
#     base_name, ext = os.path.splitext(filename)
#     return f'UserInFo/{instance}/{instance}{ext}'


class ContactManager(models.Manager):
    # def search(self, user, name='', family='', email='', phone='', num_company_or_home='', address='',
    #            ):
    #     lookup = Q(name__icontains=name) & Q(family__icontains=family) & Q(email__icontains=email) & Q(
    #         phone__icontains=phone) & Q(num_company_or_home__icontains=num_company_or_home) & Q(
    #         address__icontains=address)
    #     return user.contact_set.filter(lookup).distinct()

    def get_max_id_or_1(self):
        id__max = self.aggregate(models.Max('id'))['id__max']
        if id__max is not None:
            id__max += 1
        return id__max or 1

    def search_by_or_name_phone_email_family(self, user, search_by=''):
        lookup = Q(name__icontains=search_by) | Q(tel_home__icontains=search_by) | Q(
            phone__icontains=search_by)

        return self.filter(lookup, user__username=user).distinct()

    def search_by_or_name_phone_email_family_and_public(self, user, search_by=''):
        lookup = (Q(name__icontains=search_by) | Q(tel_home__icontains=search_by) | Q(
            phone__icontains=search_by)) & Q(is_public='بله')

        return self.filter(lookup, user__username=user).distinct()


class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, default='', null=True)
    tel_work = models.CharField(max_length=100, blank=True, default='', null=True)
    tel_home = models.CharField(max_length=100, blank=True, default='', null=True)
    comment = models.TextField(max_length=1000, blank=True, default='', null=True)
    is_public = models.CharField(max_length=3, default='خیر')
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
