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
        # aggregationSerializer = GroupSerializer(aggregationqueryset, many=True, **{'setfields':[groupField]})

        return aggregationqueryset
        # return aggregationSerializer.data
        # return aggregationqueryset

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


def nestedgrouping(groupFields,aggregationFields,baseModel,baseSerializer):
    nestedjson = []
    availFunctions = { 'Sum': Sum, 'Avg': Avg, 'Max': Max, 'Min':Min, 'Count': Count, 'StdDev': StdDev, 'Variance': Variance }
    GroupSerializer = createMutableSerializer(baseSerializer) # creates a MutableSerializer based on current "baseSerializer"

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

    def ObtainAggregations(fieldIndex,baseModel,filters):
        # We want to generate something like: "SELECT " + groupField + ", " + aggregationFields + " FROM " + Model + " GROUP BY " + groupField + ";"
        # select and group by groupFields[fieldIndex], applying filters

        # First obtains the group values for the current grouping field
        grouping = baseModel.objects.values(groupFields[fieldIndex]).distinct().annotate(**aggregations).filter(**filters)
        # groupingS = GroupSerializer(groupingQ, many=True, **{'setfields':[groupFields[fieldIndex]]})
        # grouping = groupingS.data

        # then calls a new iteration for each value obtained
        if fieldIndex < len(groupFields) -1: # calls a new iteration of grouping
            for group in grouping:
                filtaux = filters
                # filtaux.append({ groupFields[fieldIndex]: group[groupFields[fieldIndex]] })
                filtaux[groupFields[fieldIndex]] = group[groupFields[fieldIndex]] # append the current value of the grouping field as filter for the subgroup
                group['group_members'] = ObtainAggregations(fieldIndex+1,baseModel,filtaux)
                del filtaux[groupFields[fieldIndex]]
        else: # if no more grouping fields, obtains the members of each inner group
            for group in grouping:
                filtaux = filters
                # filtaux.append({ groupFields[fieldIndex]: group[groupFields[fieldIndex]] }) # append the current value of the grouping field as filter for the subgroup
                filtaux[groupFields[fieldIndex]] = group[groupFields[fieldIndex]] # append the current value of the grouping field as filter for the subgroup
                group['group_members'] = ObtainGroupMembers(filtaux)
                del filtaux[groupFields[fieldIndex]]
        return grouping

    # for each group obtained, makes a select with the list of (groupField,value) pairs in the WHEN clause, so it returns the set of individuals of
    # such a group. These are appended in the 'group_members' field of the group object. (observation: the groupFields are not included in the SELECT
    # of the individuals queries -since they are already listed in the nested groups containing the collection)
    def ObtainGroupMembers(filters):
        # We need also to define a new serializer based on the modelserializer, that excludes "groupField"
        queryset = baseModel.objects.all().filter(**filters)
        serializer = GroupSerializer(queryset, many=True, delfields=groupFields)
        return serializer.data

    # obtains the resultset produced by the aggregation query (i.e, a row for each value of groupField, where the fields shown are
    # both the groupField and the aggregationFields -such as Sum(cost)- )
    nestedjson = ObtainAggregations(0,baseModel,{}) # recursive method, obtains the final json

    return nestedjson
