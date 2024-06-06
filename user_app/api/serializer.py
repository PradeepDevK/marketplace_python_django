# from django.contrib.auth.models import User
from user_app.models import User
from rest_framework import serializers
from django.db import models


"""
Registration Serializer
"""
class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'role', 'email', 'password', 'password2',]
        extra_kwargs = {
            'password': { 'write_only': True }
        }
        
    def save(self):
        
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error': 'Passwords must match.'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'This email has already been registered.'})
        
        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            role=self.validated_data['role'],
        )
        account.set_password(self.validated_data['password'])
        account.save()
        
        return account