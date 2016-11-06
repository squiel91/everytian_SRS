from django.db import models
from mongoengine import *
import json

class User(Document):
	email = EmailField(max_length=100, required=True, primary_key=True, unique=True)
	password = StringField(max_length=100)
	name = StringField(max_length=100)

	def __str__(self):
		return self.email

class Word(Document):
	hanzi = StringField(primary_key=True, required=True, max_length=50, unique=True)
	pinyin = StringField(max_length=200)
	definitions = ListField(StringField(), default=list)

	def __str__(self):
		return self.hanzi


# from django.db import models
# import pdb
# from django_unixdatetimefield import UnixDateTimeField


# class Word(models.Model):
# 	hanzi = models.CharField(primary_key=True, max_length=50)
# 	pinyin = models.CharField(max_length=200)
# 	definitons = models.TextField()

# 	def __str__(self):
# 		return self.hanzi

# class Text(models.Model):
# 	text = models.TextField()
# 	transaltion = models.TextField()

# 	def __str__(self):
# 		return ''.join(json.loads(self.text))

# 	def raw(self):
# 		return self.text

# class User(models.Model):
# 	nick = models.CharField(primary_key=True, max_length=50)
# 	email = models.CharField(unique=True, max_length=100, null=True)

# 	def __str__(self):
# 		return self.nick