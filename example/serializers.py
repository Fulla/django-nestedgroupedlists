 # -*- coding: utf-8 -*-
from rest_framework import serializers
from example.models import Citizen

class CitizenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Citizen
        fields = ('name', 'age', 'city')
