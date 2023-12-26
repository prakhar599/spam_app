from django.urls import path
from .views import UserRegistrationView, ContactSearchView, SearchByNameView, SearchResultDetailView, SearchByPhoneNumberView, MarkAsSpamView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('search/', ContactSearchView.as_view(), name='search'),
    path('mark-as-spam/<int:phone_number>/', MarkAsSpamView.as_view(), name='mark-as-spam'),
    path('search-by-phone/', SearchByPhoneNumberView.as_view(), name='search-by-phone'),
    path('search-by-name/', SearchByNameView.as_view(), name='search-by-name'),
    path('search-result/<int:pk>/', SearchResultDetailView.as_view(), name='search-result-detail'),

]

