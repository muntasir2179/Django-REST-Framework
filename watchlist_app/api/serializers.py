from rest_framework import serializers
from watchlist_app.models import Movie


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"  # ['id', 'name', 'description', 'active']
        # exclude = ['active']   # we can exclude specific fields which we don't want to be used
    
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
