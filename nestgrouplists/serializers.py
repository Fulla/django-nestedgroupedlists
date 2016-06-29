 # -*- coding: utf-8 -*-
from django.forms import widgets
from rest_framework import serializers

# defines a generic serializerclas, which will be based in the "BaseSerializer" passed as parameter
def createMutableSerializer(BaseSerializer):

    """
    #     A MutableSerializer is a generic ModelSerializer that inherits from
    #     a given BaseSerializer, and allows it to limit the fields that are
    #     to be serialized.
    """
    class MutableSerializer(BaseSerializer):
        def __init__(self, *args, **kwargs):
            setf = kwargs.pop('setfields',None)
            delf = kwargs.pop('delfields',None)
            super(MutableSerializer, self).__init__(*args, **kwargs)
            if(setf):
                self.defineFields(setf)
            if(delf):
                self.excludeFields(delf)

        # exclude "exclFields" from the serialized fields
        def excludeFields(self,exclFields):
            # self.fields = self.fields - exclFields
            for field in exclFields:
                self.fields.pop(field)

        # limit the serialized fields only to "fields"
        def defineFields(self,fields):
            currfields = set(self.fields.keys())
            wantedfields = set(fields)
            for fi in currfields - wantedfields:
                self.fields.pop(fi)

        def getFields(self):
            return self.fields

    return MutableSerializer
