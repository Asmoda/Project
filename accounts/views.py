# -*- coding: utf-8 -*-
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from accounts.tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from accounts.forms import SignUpForm
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm


def login_user(request):
    signup_form = SignUpForm()

    if request.method == 'POST':
        login_form = AuthenticationForm(request, data=request.POST)
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if login_form.is_valid():

            user = authenticate(username=username, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('/')
    else:
        login_form = AuthenticationForm(request)

    context = {'form': login_form}
    return render(request, 'login.html', context)


def signup_user(request):
    login_form = AuthenticationForm(request)

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Mysite Account'
            message = render_to_string('account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
    else:
        signup_form = SignUpForm()

    context = {'form': signup_form}
    return render(request, 'signup.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'signup.html')
