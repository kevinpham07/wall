from __future__ import unicode_literals
from django.db import models
import re

# Create your models here.

class User(models.Model):
	first_name = models.CharField(max_length = 255)
	last_name = models.CharField(max_length = 255)
	email = models.CharField(max_length = 255)
	password = models.CharField(max_length = 255)

class Message(models.Model):
	content = models.TextField()
	user = models.ForeignKey(User, related_name = "messages")
	created_at = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
	content = models.TextField()
	message = models.ForeignKey(Message, related_name = "comments")
	creator = models.ForeignKey(User, related_name = "comments")
	created_at = models.DateTimeField(auto_now_add = True)