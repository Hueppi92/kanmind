from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.authtoken.models import Token


User = get_user_model()


class RegistrationSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    repeated_password = serializers.CharField(min_length=8, write_only=True)

    def validate_fullname(self, value):
        fullname = ' '.join(value.split())
        if len(fullname.split()) < 2:
            raise serializers.ValidationError(
                'Please provide your first name and last name.'
            )
        return fullname

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                'A user with this email address already exists.'
            )
        return email

    def validate(self, attrs):
        if attrs['password'] != attrs['repeated_password']:
            raise serializers.ValidationError(
                {'repeated_password': 'The passwords do not match.'}
            )
        return attrs

    def create(self, validated_data):
        fullname = validated_data.pop('fullname')
        validated_data.pop('repeated_password')
        first_name, *last_name = fullname.split()
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=first_name,
            last_name=' '.join(last_name),
        )
        Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs['email'].lower()
        user_record = User.objects.filter(email__iexact=email).first()
        user = authenticate(
            username=user_record.username if user_record else email,
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError('Invalid email or password.')
        attrs['email'] = email
        attrs['user'] = user
        return attrs