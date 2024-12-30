from rest_framework import serializers
from watchlist_app.models import Movie


def name_length(value):
    if len(value) < 2:
        raise serializers.ValidationError("Name is too short!")


class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(validators=[name_length])   # we can add validator functions that can be used to validate the field data
    description = serializers.CharField()
    active = serializers.BooleanField()

    # overriding the create method to perform dat insertion logic
    def create(self, validated_data):
        """_summary_

        Args:
            validated_data (object): deserialized data which is sent through the api request

        Returns:
            object: a model object created using the data sent through the api request
        """
        return Movie.objects.create(**validated_data)


    # overriding the update method to perform data update logic
    def update(self, instance, validated_data):
        """_summary_

        Args:
            instance (object): old data
            validated_data (object): updated data sent through api request

        Returns:
            object: updated model object data
        """
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.active = validated_data.get('active', instance.active)
        instance.save()
        return instance


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

