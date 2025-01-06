from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    # overriding the save() method to inject our custom logic to match password and check uniqueness of email
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:  # checking if both password are same or not
            raise serializers.ValidationError({'error': 'Both password have to be same!'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():  # checking if the email is already in use or not
            raise serializers.ValidationError({'error': 'This email already in use!'})
        
        account = User(email=self.validated_data['email'], username=self.validated_data['username'])  # creating a user with the validated data
        account.set_password(password)   # setting the password
        account.save()
        
        return account