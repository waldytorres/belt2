from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 3:
            errors["first_name"] = "Field first name should be more than 3 characters"
        if len(postData['lastname']) < 5:
            errors["last_name"] = "Field last name should be more than 3 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['emails'] = 'Invalid Email'
        if len(postData['password']) < 3:
            errors["pword"] = "Field password should be more than 3 characters"
        if (postData['confirm_password']) != (postData['password']):
            errors["confirm_pw"] = 'Password fields dont match'
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['email']):
            errors['emails'] = 'Email invalid'
        users = User.objects.filter(email=postData['email'])    
        if len(users) == 0:
            errors['user_exists'] = 'Account does not exist'
        if len(users) != 0:
            password = users[0].password
            if bcrypt.checkpw(postData['password'].encode(), password.encode()) != True:
                errors['password'] = 'Invalid password'    
        return errors


# class QuoteManager(models.Manager):
#     def quote_validator(self, postData):
#         errors = {}
#         if len(postData["quotecreator"]) < 3:
#             errors["quotescreator"] = "This Field should contain more than 3 characters"
#         if len(postData['itemname']) < 10:
#             errors["itemsname"] = "This Field should contain more than 10 characters"
#         return errors

    # *************************
    # Connect an instance of BlogManager to our Blog model overwriting
    # the old hidden objects key with a new one with extra properties!!!
    

#  if result[0]['password'] == hash1
#                 session["status"] = True

class User(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Quote(models.Model):
    itemname = models.CharField(max_length=255)
    user_items = models.ManyToManyField(User, related_name="wishlist")
    creator = models.ForeignKey(User, related_name="items_creator")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()