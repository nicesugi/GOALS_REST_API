from rest_framework import serializers
from users.models import User


class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, *args, **kwargs):
        user = super().create(*args, **kwargs)
        pw = user.password
        user.set_password(pw)
        user.save()
        return user

    class Meta:
        model = User
        fields = "__all__"
