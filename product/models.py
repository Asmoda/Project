# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    price = models.PositiveIntegerField(
        default=0
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
    )
