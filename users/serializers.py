from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data['email'])
        if user:
            raise serializers.ValidationError("Email '" + self.cleaned_data['email'] + "' znajduje sie juz w bazie")
        else:
            user = User(
                email=validated_data["email"],
                username=validated_data["username"]
            )
            user.set_password(validated_data["password"])
            user.save()
        return user

