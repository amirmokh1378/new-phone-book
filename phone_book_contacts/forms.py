from django import forms
from .models import Contact, ContactFile


class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['user']

    def save(self, user, commit=True):
        obj = super(CreateContactForm, self).save(commit=False)
        obj.user = user
        obj.id = Contact.objects.get_max_id_or_1()
        obj.save()


class AddFileForm(forms.ModelForm):
    class Meta:
        model = ContactFile
        fields = '__all__'
        exclude = ['user']
