# SpamApp - Django Project

SpamAPP is a Django-based project that helps users manage and protect against spam contacts. It provides user registration, authentication, and contact management features.

## Table of Contents

- [Introduction]
- [Features]
- [Prerequisites]
- [Installation]
- [Configuration]
- [Usage]
- [API Endpoints]
- [Testing]
- [Contributing]
- [License]
- [Acknowledgments]

## Introduction

SpamAPP is designed to simplify the management of contacts and protect users from spam. It offers a user-friendly interface for handling contacts, marking spam, and searching for contacts by various criteria.

## Features

- User registration with JWT-based authentication.
- Contact management, including marking as spam and searching by name or phone number.
- JWT-based authentication for secure user access.
- API endpoints for user registration, authentication, and contact management.

## Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Python 3.x
- Django
- Pip (Python package installer)
- DRF
- djangorestframework-simplejwt
- djangorestframework

## Installation

To install the project dependencies, run the following command:

```bash
pip install -r re.txt

## Configuration
Before running the project, configure the database settings in the settings.py file. Ensure the database is set up and migrate the initial schema using:

- python manage.py migrate
For security reasons, set the SECRET_KEY in settings.py to a unique and secure value.

##   Usage
Start the Django development server:
- python manage.py runserver
- Access the application at http://localhost:8000 in your web browser.

## API Endpoints
The following API endpoints are available:

/api/register/: User registration.
/api/login/: User login and token retrieval.
/api/contacts/: List and create contacts.
/api/contacts/{phone_number}/mark-as-spam/: Mark a contact as spam.
