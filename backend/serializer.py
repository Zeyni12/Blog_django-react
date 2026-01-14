from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPariSerializer
from rest_framework import serializers

from api import models as api_models

class MyTokenObtainPairSerializer(TokenObtainPariSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.charField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.charField(write_only=True, required=True)
    
    class Meta:
        models = api_models.User
        fields = ['full_name','email','password','password2']
        
    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({'password':'password fields didnt match'}) 
        
        return attr  
    
    def create(self, validated_data):
        user = api_models.User.objects.create(
            full_name = validated_data['full_name'],
            email = validated_data['email'],
        ) 
        
        email_