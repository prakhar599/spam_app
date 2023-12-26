from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Contact

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'email', 'password']

    def create(self, validated_data):
        # Hash the password before saving it to the database
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def get_email(self, obj):
        # Retrieve the request user from the serializer context
        request_user = self.context.get('request_user')
        
        # Check if the request user is authenticated and matches the object
        if request_user and request_user.is_authenticated and obj == request_user:
            return obj.email
        else:
            return None

# Serializer for the Contact model
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'spam_likelihood', 'detail_url', 'email']

    # Hyperlinked identity field for generating detail URLs
    detail_url = serializers.HyperlinkedIdentityField(
        view_name='search-result-detail',
        lookup_field='pk'
    )

    # Serializer method field for retrieving email based on conditions
    email = serializers.SerializerMethodField()
    
    def get_email(self, obj):
        # Retrieve the request user from the serializer context
        request_user = self.context.get('request_user')
        
        # Check if obj.user is an instance of User before accessing email
        if isinstance(obj.user, User) and obj.user == request_user:
            return obj.user.email
        else:
            return None
