# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Product():
    user = models.OneToOneField(User, on_delete=models.CASCADE)
	price = models.PositiveIntegerField(
		default=0
	)
	name = charfield