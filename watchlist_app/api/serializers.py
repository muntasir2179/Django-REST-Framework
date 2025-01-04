from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Reviews
        exclude = ("watchlist",)


class WatchListSerializer(serializers.ModelSerializer):
    # using the previously set related_name to fetch review data
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):
    # this field name must match with the predefined related_name in model relationship field
    watchlist = WatchListSerializer(many=True, read_only=True)   # it will serialize all the data from the related model
    class Meta:
        model = StreamPlatform
        fields = "__all__"