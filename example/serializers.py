 # -*- coding: utf-8 -*-
from rest_framework import serializers
from example.models import Citizen, CitizenExt

class CitizenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizen
        fields = ('name', 'age', 'city')

class CitizenExtSerializer(serializers.ModelSerializer):

    class Meta:
        model = CitizenExt
        fields = ('name', 'age', 'gender','country','city')
