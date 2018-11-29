from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9copy.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_login(self, postData):
        errors = {}
        if len(postData['username']) < 1:
            errors['username'] = 'Invalid username...'
        elif len(User.objects.filter(username=postData['username'])) == 0:
            errors['username'] = 'Username is not registered...'
        if len(postData['password']) < 1:
            errors['password'] = 'Password cannot be blank...'
        elif len(User.objects.filter(username=postData['username'])) != 0:
            user = User.objects.get(username=postData['username'])
            if bcrypt.checkpw(postData['password'].encode(), user.password_hash.encode()) == False:
                errors['login'] = 'Email and password do not match...'
        return errors
    
    def validate_register(self, postData):
        errors = {}
        if len(postData['reg_username']) < 3:
            errors['username'] = 'Username must be at least 3 characters...'
        if len(postData['reg_email']) < 1 or not EMAIL_REGEX.match(postData['reg_email']):
            errors['email'] = 'Invalid email...'
        elif len(User.objects.filter(email=postData['reg_email'])) != 0:
            errors['email'] = 'Email already taken...'
        if len(postData['reg_password']) < 8:
            errors['password'] = 'Password must be at least 8 characters...'
        elif postData['confirm_password'] != postData['reg_password']:
            errors['confirm_password'] = "Passwords don't match..."
        return errors

class User(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=255)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Question(models.Model):
    user = models.ForeignKey(User, related_name='user_questions')
    question = models.TextField()
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Response(models.Model):
    user = models.ForeignKey(User, related_name='user_responses')
    question = models.ForeignKey(Question, related_name='question_responses')
    content = models.TextField()
    code = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Followship(models.Model):
    follower = models.ForeignKey(User, related_name="following")
    followee = models.ForeignKey(User, related_name="followed")
    created_at = models.DateTimeField(auto_now_add=True)