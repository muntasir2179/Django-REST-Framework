from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    len_name = serializers.SerializerMethodField()    # we can define a read only field which is not the part of the model but we can construct it in serializer class
    
    class Meta:
        model = Movie
        fields = "__all__"  # ['id', 'name', 'description', 'active']
        # exclude = ['active']   # we can exclude specific fields which we don't want to be used
    
    # fetching data for serializer method field
    def get_len_name(self, object):
        return len(object.name)
    
    # method for validating name field
    # field level validation
    def validate_description(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("Description is too short!")
        else:
            return value
    
    # object level validation
    def validate(self, data):
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and description should be different!")
        return data
