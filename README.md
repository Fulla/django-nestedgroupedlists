# Nested Grouped Lists

Sometimes, when we are listing members from a model, it is necessary to group the information according to the value of some field, and maybe also include some annotations for each group.

This behavior is easily achieved with the "GROUP BY" sql clause (and annotations are included adding the corresponding aggregation functions in the SELECT); or with .values() and .annotate() if we are using the django ORM.

However, when we make grouped queries, we just are able to show the field/s by which we are grouping, and so we lost group individuals.
If we want to recover the corresponding members for each group, we need to make the proper requests later.

So, for example, if we have a model for Citizen, and want to list them but also include the "average" age of the citizens distinguished by "city",
we need to make a ORM query similar to Citizen.values('city').annotate(Avg('age')),
and then make the corresponding queries to obtain the citizens of each city.

Won't it be **great** to make just one request, -indicating which is the field by which want to group the individuals and which are the aggregation functions we want to show-, and obtain a JSON with both the grouping information and the individuals nested in each group?

## Mode of use:

Well, this api makes that. It provides you with a function (simplegrouping) that you will call indicating
- 1: groupField = the name of the field the data will be grouped by
- 2: aggregationFields = list of aggregation functions that we want to show for the groups.
     Each element in the list is in the format {'function':'Func', 'field': 'Field'}
      * Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
      * Field is the field of your model over which the function is applied
- 3: model = model over wich the request is made
- 4: serializer = model serializer

For example, we call
```
  simplegrouping('city', [{'Count','id'},{'Avg','age'}], Citizen, CitizenSerializer)
```

and we obtain a JSON were, for each group, there is a field for each aggregation function and a field for the list of members of the group.

```
  [
   {
     'city': 'Kansas',
     'Count_id': 2,
     'Avg_age': 53,
     'group_members': [
        	{ 'id': 2, 'name': 'Tom', 'age': 85 },
         	{ 'id': 5, 'name': 'Will', age: 21 }
      ]
   },
   {
     'city': 'Bristol',
     'Count_id': 1,
     'Avg_age': 35,
     'group_members': [
          { 'id': 1, 'name': 'Phil', 'age': 35 }
      ]
   },
   {
     'city': 'Hannover',
     'Count_id': 3,
     'Avg_age': 26,
     'group_members': [
        	{ 'id': 3, 'name': 'Rossana', 'age': 27 },
         	{ 'id': 4, 'name': 'Thelma', 'age': 20 },
        	{ 'id': 6, 'name': 'Roger', 'age': 31 }
      ]
   }
  ]
```
