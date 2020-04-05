from rest_framework import serializers
from .models import Account, CorpsMember

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            'id', 
            'email',
            'password',
            'created_ts',
            'last_ts',
        ]

    def create(self, validated_data):
        return Account.init(**validated_data)


    def update(self, instance: Account, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance
