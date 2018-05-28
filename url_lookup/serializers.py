from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import URLBlacklist
from .utils import check_availability


class URLInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    url = serializers.CharField(required=True, max_length=500, allow_null=False, allow_blank=False)
    is_restricted = serializers.BooleanField(default=True, required=False)

    def create(self, validated_data):
        """
        Create and return the `URLBlacklist` instance
        :param validated_data:
        :return:
        """
        # Check whether the URL already exists
        is_exists, url_obj = check_availability(validated_data.get('url'))
        if is_exists:
            return True, None
        new_obj = URLBlacklist()
        new_obj.url = validated_data.get('url')
        new_obj.is_restricted = validated_data.get('is_restricted', True)
        new_obj.save()
        return False, new_obj

    def update(self, instance, validated_data):
        instance.url = validated_data.get('url')
        instance.is_restricted = validated_data.get('is_restricted', True)
        instance.save()
        return instance
