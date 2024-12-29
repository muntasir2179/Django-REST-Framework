from rest_framework import serializers
from watchlist_app.models import Movie

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
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

