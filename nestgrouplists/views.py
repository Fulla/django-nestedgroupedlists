# -*- coding: utf-8 -*-
from django.shortcuts import render
from rest_framework import generics
from nestgrouplists.serializers import createMutableSerializer
from django.db.models import Sum, Avg, Max, Min, Count, StdDev, Variance

# Create your views here.

# Makes the necessary queries to obtain both the aggregation information (grouping by groupField),
# and the rows of each group. Then, with such information, generates the corresponding nested json representation

# SIMPLE GROUPING - Params
## 1: groupField = the name of the field the data will be grouped by
## 2: aggregationFields = list of aggregations, where each element in the list is in the format {'function':'Func', 'field': 'Field'}
    # Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
    # Field is the field of your model over which the function is applied
## 3: baseModel = model over wich the request is made
## 4: baseSerializer = model serializer for the baseModel
def simplegrouping(groupField,aggregationFields,baseModel,baseSerializer):
    nestedjson = []
    availFunctions = { 'Sum': Sum, 'Avg': Avg, 'Max': Max, 'Min':Min, 'Count': Count, 'StdDev': StdDev, 'Variance': Variance }
    GroupSerializer = createMutableSerializer(baseSerializer) # creates a MutableSerializer based on current "baseSerializer"

    def ObtainAggregation(groupField,aggregationFields,baseModel):
        # We want to generate something like: "SELECT " + groupField + ", " + aggregationFields + " FROM " + Model + " GROUP BY " + groupField + ";"
        # select and group by groupField
        aggregations = {} # Stores the annotations in a dictionary, that later is passed to the annotate (in the query) as **kwargs
        for aggF in aggregationFields:
            field = aggF['field']
            func = aggF['function']
            alias = func +"_"+ field
            if (availFunctions[func]):
                aFunction = availFunctions[func]
                aggregations[alias] = (aFunction(field))
            else:
                print 'Annotated function '+func+' does not exist'

        aggregationqueryset = baseModel.objects.values(groupField).distinct().annotate(**aggregations)
        aggregationSerializer = GroupSerializer(aggregationqueryset, many=True, **{'setfields':[groupField]})

        print aggregationSerializer.data
        return aggregationqueryset

    def ObtainGroupMembers(value):
        # We need also to define a new serializer based on the modelserializer, that excludes "groupField"
        queryset = baseModel.objects.all().filter(**{groupField: value})
        serializer = GroupSerializer(queryset, many=True, delfields=[groupField])
        return serializer.data

    # obtains the resultset produced by the aggregation query (i.e, a row for each value of groupField, where the fields shown are
    # both the groupField and the aggregationFields -such as Sum(cost)- )
    nestedjson = ObtainAggregation(groupField,aggregationFields,baseModel)

    # then, for each group obtained, makes a select with the current groupField value in the WHEN clause, so it returns the set of individuals of
    # such a group. These are appended in the 'individuals' field of the group object. (observation: groupField is not included in the SELECT
    # of the individuals queries -since it is already in the object containing the collection)
    for group in nestedjson:
        value = group[groupField]
        group['group_members'] = ObtainGroupMembers(value)

    return nestedjson
