from rest_framework import serializers
from .models import User, Requests

class UserSerializer( serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
        extra_kwargs={
            'password':{'write_only':True}
        }

    def create(self, validated_data):
        password= validated_data.pop('password',None)
        instance= self.Meta.model(**validated_data)
        if password is not True:
            instance.set_password(password)
        instance.save()
        return instance


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=Requests
        fields = ['rid','name', 'email', 'message']