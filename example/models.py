# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Citizen(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    age = models.IntegerField(blank=False)
    city = models.CharField(max_length=50, blank=False)

    # class Meta:
    #     app_label = "example"

class CitizenExt(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=False)
    age = models.IntegerField(blank=False)
    gender = models.CharField(
        max_length=1,
        choices=(
            ('M','male'),
            ('F','female')
        ),
        default='F'
    )
    country = models.CharField(max_length=50, blank=False)
    city = models.CharField(max_length=50, blank=False)

    # class Meta:
    #     app_label = "example"
