from django import forms
from .models import Contact, ContactFile


class CreateContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        exclude = ['user']

    def save(self, user, id, commit=True):
        obj = super(CreateContactForm, self).save(commit=False)
        obj.user = user
        if id is None:
            obj.id = Contact.objects.get_max_id_or_1()
        else:
            obj.id=id
        obj.save()


class AddFileForm(forms.ModelForm):
    class Meta:
        model = ContactFile
        fields = '__all__'
        exclude = ['user']
