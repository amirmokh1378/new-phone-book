from django import forms
from django.core import validators
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید'}),
                                label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را وارد کنید'}),
                               label='رمز عبور')


class RegisterForm(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'نام کاربری خود را وارد کنید'}),
                                label='نام کاربری',
                                validators=[
                                    validators.MinLengthValidator(4, 'تعداد کارکتر ها باید بیشتر از4 تا باشند'),
                                    validators.MaxLengthValidator(30, 'طولش نباید بیشتر از 30 بشود'),
                                ]
                                )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور خود را وارد کنید'}),
                               label='رمز عبور',
                               validators=[
                                   validators.MinLengthValidator(4, 'تعداد کارکتر ها باید بیشتر از4 تا باشند'),
                                   validators.MaxLengthValidator(30, 'طولش نباید بیشتر از 30 بشود'),
                               ]
                               )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور را دوباره وارد نماید'}),
        label='تایید عبور')

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}),
                             label='E-mail',
                             validators=[validators.EmailValidator('ایمیل معتبر نمیباشد')])

    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        dose_user_exist_by_user_name = User.objects.filter(username=user_name).exists()
        if dose_user_exist_by_user_name:
            error = forms.ValidationError('این نام کاربری قبلا استفاده شده است')
            raise error
        if ' ' in user_name:
            error = forms.ValidationError('نباید در نام کاربری فاصله وجود داشته باشد')
            raise error
        return user_name

    def clean_email(self):
        email = self.cleaned_data['email']
        dose_user_exist_by_email = User.objects.filter(email=email).exists()
        if dose_user_exist_by_email:
            error = forms.ValidationError('این ایمیل قبلا استفاده شده است')
            raise error
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        co_password = self.cleaned_data['confirm_password']
        print(co_password, password)
        if password != co_password:
            raise forms.ValidationError('پسورد و تایید پسورد یکسان نیستند')
        return co_password


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'text']
        # exclude = '__all__'

    def save(self, id, commit=False):
        user = User.objects.get(id=id)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.image = self.cleaned_data['image']
        user.text = self.cleaned_data['text']
        user.save()


    def clean_user_name(self):
        user_name = self.cleaned_data['user_name']
        dose_user_exist_by_user_name = User.objects.filter(username=user_name).exists()
        if dose_user_exist_by_user_name:
            error = forms.ValidationError('این نام کاربری قبلا استفاده شده است')
            raise error
        return user_name
