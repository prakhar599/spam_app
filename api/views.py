# Import necessary modules and classes from Django Rest Framework
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from django.db.models import Q
from django.shortcuts import get_object_or_404

# Import models and serializers from the current application
from .models import User, Contact
from .serializers import UserSerializer, ContactSerializer

# User registration view
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # Call the parent create method
        response = super().create(request, *args, **kwargs)
        # Retrieve the user object from the created data
        user = self.queryset.get(name=request.data['name'])
        # Generate tokens for the user
        refresh = RefreshToken.for_user(user)
        # Prepare the response data with access and refresh tokens
        response_data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        # Update the response data with token information
        response.data.update(response_data)
        return response

# User login view
class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if the request includes the 'refresh' key
        if 'refresh' in request.data:
            refresh = request.data.get('refresh')
            try:
                # Attempt to refresh the access token using the provided refresh token
                refresh_token = RefreshToken(refresh)
                access_token = str(refresh_token.access_token)
                response_data = {
                    'access': access_token,
                }
                # Return the refreshed access token in the response
                return Response(response_data, status=status.HTTP_200_OK)
            except Exception as e:
                # Return an error response if the refresh token is invalid
                return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            # If 'refresh' key is not present, assume it's a regular login
            name = request.data.get('name')
            password = request.data.get('password')
            # Attempt to authenticate the user using provided credentials
            user = User.objects.filter(name=name).first()
            if user and user.check_password(password):
                # If authentication is successful, generate and return tokens
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # Return an error response for invalid credentials
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Contact search view
class ContactSearchView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Retrieve the 'query' parameter from the request
        query = self.request.query_params.get('query', '')
        # Filter contacts based on name (case-insensitive) matching the query
        return Contact.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query)
        )

# Mark contact as spam view
class MarkAsSpamView(generics.UpdateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def update(self, request, *args, **kwargs):
        # Retrieve the phone number from the URL parameters
        phone_number = kwargs.get('phone_number')
        # Get the contact instance using the phone number
        instance = get_object_or_404(Contact, phone_number=phone_number)
        # Increment the spam likelihood and save the instance
        instance.spam_likelihood += 1 
        instance.save()
        # Serialize and return the updated contact data
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Search contacts by name or username view
class SearchByNameView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Retrieve the 'query' parameter from the request
        query = self.request.query_params.get('query', '')    
        # Search for users and contacts with names matching the query
        users_queryset = User.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query)
        )        
        contacts_queryset = Contact.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query)
        ).order_by('name')
        # Combine and order the results
        queryset = list(users_queryset) + list(contacts_queryset)
        return queryset

    def get_serializer_context(self):
        # Add the request user to the serializer context
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

# Search contacts by phone number view
class SearchByPhoneNumberView(generics.ListAPIView):
    serializer_class = ContactSerializer

    def get_queryset(self):
        # Retrieve the 'query' parameter from the request
        query = self.request.query_params.get('query', '')
        # Search for users and contacts with phone numbers matching the query
        users_queryset = User.objects.filter(
            Q(phone_number__exact=query)
        )
        contacts_queryset = Contact.objects.filter(
            Q(phone_number__exact=query)
        ).order_by('name')
        # Combine and order the results
        queryset = list(users_queryset) + list(contacts_queryset)
        return queryset

    def get_serializer_context(self):
        # Add the request user to the serializer context
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context

# View to retrieve detailed information about a search result (contact)
class SearchResultDetailView(generics.RetrieveAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        # Add the request user to the serializer context
        context = super().get_serializer_context()
        context['request_user'] = self.request.user
        return context
