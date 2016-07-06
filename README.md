# Nested Grouped Lists

Sometimes, when we are listing members from a model, it is necessary to group the information according to the value of some field, and maybe also include some annotations for each group.

This behavior is easily achieved with the "GROUP BY" sql clause (and annotations are included adding the corresponding aggregation functions in the SELECT); or with .values() and .annotate() if we are using the django ORM.

However, when we make grouped queries, we just are able to show the field/s by which we are grouping, and so we lost group individuals.
If we want to recover the corresponding members for each group, we need to make the proper requests later.

So, for example, if we have a model for Citizen, and want to list them but also include the "average" age of the citizens distinguished by "city",
we need to make a ORM query similar to Citizen.values('city').annotate(Avg('age')),
and then make the corresponding queries to obtain the citizens of each city.

Won't it be **great** to make just one request, -indicating which is the field by which want to group the individuals and which are the aggregation functions we want to show-, and obtain a JSON with both the grouping information and the individuals nested in each group?

## Simple grouping:

Well, this api makes that. It provides you with a function (simplegrouping) that you will call indicating
- 1: groupField = the name of the field the data will be grouped by
- 2: aggregationFields = dictionary of aggregation functions that we want to show for the groups.
     Each element in the dict is in the format `{'function':'Func', 'field': 'Field'}`
      * Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
      * Field is the field of your model over which the function is applied
- 3: model = model over wich the request is made
- 4: serializer = model serializer

For example, we call
```
  aggregations = [{'function':'Count','field':'id'},{'function':'Avg','field':'age'}]
  simplegrouping('city', aggregations, Citizen, CitizenSerializer)
```
[Citizen and CitizenSerializer are provided in example application]
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

## Nested multiple grouping:

If you want to group by multiple criteria in a nested way (for example, outer grouping by country and inner grouping by city),
the API also provides you with a function (nestedgrouping) for doing so.
The nomenclature is very similar to simplegrouping. However, in this case, you are going to provide not just the field name to group by, but a list of field names. The field names are used one by one in order of appearance as the grouping criterion for each nesting level.
The arguments in this case are:
- 1: groupFields = the list of field names the data will be iteratively grouped by.
- 2: aggregationFields = dictionary of aggregation functions that we want to show for the groups.
     Each element in the dict is in the format `{'function':'Func', 'field': 'Field'}`
      * Func is one of the followings: 'Sum', 'Avg', 'Max', 'Min', 'Count', 'StdDev', 'Variance'
      * Field is the field of your model over which the function is applied
- 3: model = model over wich the request is made
- 4: serializer = model serializer

For example, we call
```
  aggregations = [{'function':'Count','field':'id'},{'function':'Avg','field':'age'},{'function':'Sum','field':'age'}]
  nestedgrouping(['country','city'], aggregations, CitizenExt, CitizenExtSerializer)
```
[CitizenExt and CitizenExtSerializer are provided in example application]
and we obtain a JSON were, for each group, there is a field for each aggregation function and a field for the list of members of the group.

```
[
    {
        "group_members": [
            {
                "group_members": [
                    {
                        "name": "Cassie",
                        "age": 17,
                        "gender": "F"
                    },
                    {
                        "name": "Sid",
                        "age": 17,
                        "gender": "M"
                    }
                ],
                "city": "Bristol",
                "Sum_age": 34,
                "Count_id": 2,
                "Avg_age": 17.0
            }
        ],
        "country": "England",
        "Sum_age": 34,
        "Count_id": 2,
        "Avg_age": 17.0
    },
    {
        "group_members": [
            {
                "group_members": [
                    {
                        "name": "Joey",
                        "age": 29,
                        "gender": "M"
                    },
                    {
                        "name": "Chandler",
                        "age": 30,
                        "gender": "M"
                    },
                    {
                        "name": "Rachel",
                        "age": 28,
                        "gender": "F"
                    },
                    {
                        "name": "Monica",
                        "age": 28,
                        "gender": "F"
                    },
                    {
                        "name": "Ross",
                        "age": 30,
                        "gender": "M"
                    },
                    {
                        "name": "Phoebe",
                        "age": 29,
                        "gender": "F"
                    }
                ],
                "city": "New York",
                "Sum_age": 174,
                "Count_id": 6,
                "Avg_age": 29.0
            },
            {
                "group_members": [
                    {
                        "name": "Homer",
                        "age": 45,
                        "gender": "M"
                    },
                    {
                        "name": "Marge",
                        "age": 42,
                        "gender": "F"
                    },
                    {
                        "name": "Bart",
                        "age": 11,
                        "gender": "M"
                    }
                ],
                "city": "Springfield",
                "Sum_age": 98,
                "Count_id": 3,
                "Avg_age": 32.67
            }
        ],
        "country": "United States",
        "Sum_age": 272,
        "Count_id": 9,
        "Avg_age": 30.22
    }
]
```
