from rest_framework import serializers
from .models import FEmployee, SEmployee

class BaseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()    
    department = serializers.CharField()

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must be only digits.")
        return value
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.department = validated_data.get('department', instance.department)


class FEmployeeSerializer(BaseSerializer):
    designation = serializers.CharField(required=False)

    def create(self, validated_data, job):
        validated_data['source'] = job
        return FEmployee(**validated_data)

    def update(self, instance, validated_data, job):
        instance.designation = validated_data.get('designation', instance.designation)
        instance.status = 'Updated'
        instance.source = job
        # instance.save()
        return instance


class SEmployeeSerializer(BaseSerializer):
    salary = serializers.DecimalField(max_digits=7, decimal_places=2, required=False)

    def create(self, validated_data, job):
        validated_data['source'] = job
        return SEmployee(**validated_data)

    def update(self, instance, validated_data, job):
        instance.salary = validated_data.get('salary', instance.salary)
        instance.status = 'Updated'
        # instance.save()
        return instance
