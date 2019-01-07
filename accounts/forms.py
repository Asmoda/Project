from django import forms
from django.contrib.auth.forms import UserCreationForm, UserCreationForm
from django.contrib.auth.models import User
from accounts.models import UserProfile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address. ')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        user.save()

        return user

