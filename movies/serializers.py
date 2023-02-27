from email.policy import default
from rest_framework import serializers

from .models import Movie, Choices, MovieOrder

class MovieSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=127, allow_null=True)
    duration = serializers.CharField(max_length=10, allow_null=True, default=None)
    synopsis = serializers.CharField(allow_null=True, default=None)
    added_by = serializers.EmailField(read_only=True, source="user.email")

    rating = serializers.ChoiceField(
        choices=Choices.choices,
        default=Choices.G
    )

    def create(self, validated_data):
        return Movie.objects.create(**validated_data)

class MovieOrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        max_length=127,
        allow_null=True,
        read_only=True,
        source="movie.title"
    )
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    buyed_at = serializers.DateTimeField(read_only=True)
    buyed_by = serializers.EmailField(read_only=True, source="user.email")

    def create(self, validated_data):
        return MovieOrder.objects.create(**validated_data)