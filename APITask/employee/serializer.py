from rest_framework import serializers

class FEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()    
    department = serializers.CharField()
    designation = serializers.CharField(required=False)

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must be only digits.")
        return value


class SEmployeeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    email = serializers.EmailField()
    mobile = serializers.CharField()    
    department = serializers.CharField()
    salary = serializers.FloatField(required=False)

    def validate_mobile(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Mobile number must be only digits.")
        return value
