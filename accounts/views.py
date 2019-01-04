# -*- coding: utf-8 -*-
from django.db.models import Q
from .models import UserProfile
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from .forms import SignUpForm
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth.forms import AuthenticationForm

def login_user(request):
	data = dict()
	confirm_error = False
	signup_form_active = False
	data['loginned'] = False

	signup_form = SignUpForm()

	if request.method == 'POST':
		login_form = AuthenticationForm(request, data=request.POST)
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '').strip()
		if login_form.is_valid():
			data['form_is_valid'] = True

			user = authenticate(username=username, password=password)
			if user is not None:
				if user.is_active:
					login(request, user)
					data['loginned'] = True
				else:
					confirm_error=True
		else:
			data['form_is_valid'] = False
	else:
		login_form = AuthenticationForm(request)

	context = {'signup_form': signup_form, 'login_form': login_form, 'confirm_error': confirm_error,
	'signup_form_active': signup_form_active }
	data['html_form'] = render_to_string('registration/includes/partial_signup_create.html',
		context,
		request=request
	)
	return JsonResponse


def signup_user(request):
    data = dict()
    signup_form_active = True
    login_form = AuthenticationForm(request)

    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        if signup_form.is_valid():
            data['form_is_valid'] = True
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Mysite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

        else:
            data['form_is_valid'] = False
    else:
        signup_form = SignUpForm()

    context = {'signup_form': signup_form, 'login_form': login_form, 'signup_form_active': signup_form_active}
    data['html_form'] = render_to_string('registration/includes/partial_signup_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


def account_activation_sent(request):
    return render(request, 'registration/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.userprofile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/')
    else:
        return render(request, 'registration/account_activation_invalid.html')
# Create your views here.
