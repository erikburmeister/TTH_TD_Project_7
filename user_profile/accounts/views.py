from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from PIL import Image

from .models import User
from .forms import (AccountSignUpForm, AccountUpdateForm,
                    AccountImageUpdateForm, UserUpdateForm,
                    ChangePasswordForm)


def account_home(request):
    return render(request, 'accounts/home.html')


@login_required
def view_account(request, username):
    user = User.objects.get(username=username)
    context = {'user': user}
    return render(request, 'accounts/account.html', context)


@login_required
def edit_account(request, username):
    if request.method == 'POST':
        user_update_form = UserUpdateForm(request.POST,
                                          instance=request.user)
        account_update_form = AccountUpdateForm(
            request.POST,
            instance=request.user.account
        )

        image_update_form = AccountImageUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.account
        )

        if (user_update_form.is_valid() and
            account_update_form.is_valid() and
            image_update_form.is_valid()):

            user_update_form.save()
            account_update_form.save()
            image_update_form.save()
            messages.success(request,
                             "Your account has been updated!")
            return HttpResponseRedirect(
                        reverse('accounts:accounts-account',
                            kwargs={
                                'username': request.user.username
                            }))

    else:
        user_update_form = UserUpdateForm(
            instance=request.user)
        account_update_form = AccountUpdateForm(
            instance=request.user.account)
        image_update_form = AccountImageUpdateForm(
            instance=request.user.account)

    context = {'user_update_form': user_update_form,
               'account_update_form': account_update_form,
               'image_update_form': image_update_form}

    return render(request, 'accounts/edit_account.html', context)


@login_required
def edit_avatar(request, username):
    user = User.objects.get(username=username)

    if request.method == 'POST':
        image_update_form = AccountImageUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user.account)

        if image_update_form.is_valid():
            image_update_form.save()
            return HttpResponseRedirect(
                reverse('accounts:accounts-account',
                        kwargs={
                            'username': request.user.username
                        }))
    else:
        image_update_form = AccountImageUpdateForm(
            instance=request.user.account)

    context = {'user': user,
               'image_update_form': image_update_form}
    return render(request, 'accounts/edit_avatar.html', context)


def change_password(request, username):
    if request.method == 'POST':
        change_password_form = ChangePasswordForm(
            request.user, request.POST)

        if change_password_form.is_valid():
            user = change_password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request,
                             "Your password has been updated!")
            return HttpResponseRedirect(
                reverse('accounts:accounts-account',
                        kwargs={'username': request.user.username}))

    else:
        change_password_form = ChangePasswordForm(request.user)

    context = {'change_password_form': change_password_form}
    return render(request, 'accounts/change_password.html', context)


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    username = request.user.username
                    return HttpResponseRedirect(
                        reverse('accounts:accounts-account',
                                kwargs={'username': username})
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = AccountSignUpForm()
    if request.method == 'POST':
        form = AccountSignUpForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            username = request.user.username
            return HttpResponseRedirect(
                reverse('accounts:accounts-account',
                        kwargs={'username': username}))

    return render(request, 'accounts/sign_up.html', {'form': form})

@login_required
def sign_out(request):
    logout(request)
    messages.success(request,
                     "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('accounts:accounts-home'))
