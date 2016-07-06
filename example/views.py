# -*- coding: utf-8 -*-

from django.shortcuts import render
from nestgrouplists.views import *
from example.serializers import CitizenSerializer, CitizenExtSerializer
from example.models import Citizen, CitizenExt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.

# Method using nested-grouped-listing with annotations
@api_view(['GET'])
def ListGrouped(request):
    aggFields = [
        {'function': 'Count', 'field': 'name'},
        {'function': 'Sum', 'field': 'age'}
    ]

    # SIMPLE GROUPING - Params
    ## 1: field to group by
    ## 2: list of aggregations, where each element in the list is in the format {'function':'Func', 'field': 'Field'}
        # Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
        # Field is the field of your model over which the function is applied
    ## 3: model over wich the request is made
    ## 4: modelserializer for the model
    listgrouped = simplegrouping('city', aggFields, Citizen, CitizenSerializer)
    return Response(listgrouped)

# Method using nested-grouped-listing with annotations
@api_view(['GET'])
def NestListGrouped(request):
    aggFields = [
        {'function': 'Count', 'field': 'name'},
        {'function': 'Sum', 'field': 'age'},
        {'function': 'Avg', 'field': 'age'}
    ]

    # NESTED MULTIPLE GROUPING - Params
    ## 1: fields to group by
    ## 2: list of aggregations, where each element in the list is in the format {'function':'Func', 'field': 'Field'}
        # Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
        # Field is the field of your model over which the function is applied
    ## 3: model over wich the request is made
    ## 4: modelserializer for the model
    listgrouped = nestedgrouping(['country','city'], aggFields, CitizenExt, CitizenExtSerializer)
    return Response(listgrouped)

# Class using standar listing
class CitizenView(generics.ListCreateAPIView):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer

# Class using standar listing
class CitizenExtView(generics.ListCreateAPIView):
    queryset = CitizenExt.objects.all()
    serializer_class = CitizenExtSerializer
