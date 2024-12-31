from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # this field name must match with the predefined related_name in model relationship field
    watchlist = WatchListSerializer(many=True, read_only=True)   # it will serialize all the data from the related model
    class Meta:
        model = StreamPlatform
        fields = "__all__"