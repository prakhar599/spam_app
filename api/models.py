from django.db import models

class User(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)

    def check_password(self, raw_password):
        # Implement password checking logic
        return raw_password == self.password

    def __str__(self):
        return self.name

class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    spam_likelihood = models.IntegerField(default=0)
    def __str__(self):
        return self.name
