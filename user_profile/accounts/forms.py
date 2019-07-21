from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm

import re

from .models import User, Account

class AccountSignUpForm(UserCreationForm):
    first_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=False, max_length=50)
    email = forms. EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

        help_texts = {
            'id_password1': None,
            'password2': None,
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    confirm_email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'confirm_email')

    def clean(self):
        email = self.cleaned_data.get('email')
        confirm_email = self.cleaned_data.get('confirm_email')

        if email != confirm_email:
            raise forms.ValidationError(
                'Email fields are not the same.')


class DateInput(forms.DateInput):
    input_type = 'date'


class AccountUpdateForm(forms.ModelForm):

    bio = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'mytextarea'}), required=False)

    class Meta:
        model = Account
        fields = ('date_of_birth', 'city', 'state', 'country',
                  'favorite_animal', 'favorite_hobby',
                  'favorite_movie', 'bio')
        widgets = {'date_of_birth': DateInput()}

    def clean(self):
        bio = self.cleaned_data['bio']

        if len(bio) < 17:
            raise forms.ValidationError(
                'Bio needs to have a minimum of 10 characters in it.')


class AccountImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['avatar']


class ChangePasswordForm(PasswordChangeForm):
    def clean(self):
        cleaned_data = super().clean()

        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password1')
        confirm_password = cleaned_data.get('new_password2')
        print("Old password: ", old_password)
        print("New password: ", new_password)
        print("Confirm password: ", confirm_password)
        print(self.user.first_name)
        print(self.user.last_name)
        print(self.user.username)

        user = self.user
        if user.check_password(new_password):
            raise forms.ValidationError(
                "Must not be the same as the current password.")

        if len(new_password) < 14:
            raise forms.ValidationError(
                "Minimum password length of 14 characters.")

        if (new_password == new_password.upper() or
                new_password == new_password.lower()):
            raise forms.ValidationError(
                "Must use of both uppercase and lowercase letters.")

        if not re.search(r'\d', new_password):
            raise forms.ValidationError(
                "Must include one or more numerical digits.")

        if not re.search(r'\W', new_password):
            raise forms.ValidationError(
                """Must include one or more of
                special characters, such as @, #, $.""")

        if (user.first_name.lower() in new_password.lower() or
            user.last_name.lower() in new_password.lower() or
            user.username.lower() in new_password.lower()):
            raise forms.ValidationError(
                """cannot contain the user name or parts of the user’s
                full name, such as their first name""")

