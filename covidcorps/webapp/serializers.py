from rest_framework import serializers
from . import models

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Account
        fields = [
            'id', 
            'email',
            'password',
            'active',
            'created_ts',
            'last_ts',
        ]

    def create(self, validated_data):
        a = Account.init(**validated_data)
        a.save()
        return a

    def update(self, instance: models.Account, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class CorpsMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CorpsMember
        fields = [
            'id',
            'account',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'suffix',
            'address1',
            'address2',
            'city',
            'state',
            'zipcode',
            'active',
            'category',
            'deployments',
            'created_ts',
            'last_ts',
        ]

class CorpsMemberPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CorpsMemberPhoneNumber

class CorpsMemberEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CorpsMemberEmail

