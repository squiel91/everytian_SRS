from django.db import models
from mongoengine import *
import json

pronunciations = ('tonal', 'numeric', 'bopomofo')

class User(Document):
	email = EmailField(max_length=100, required=True, primary_key=True, unique=True)
	name = StringField(max_length=25, required=True)
	password = StringField(max_length=100)
	simplified = BooleanField()
	pronunciation = StringField(max_length=20, choices=pronunciations)
	verified_email = BooleanField(default=False)
	verify_email_token = IntField(default=1234)

	def __str__(self):
		return self.email

class Word(Document):
	hanzi = StringField(primary_key=True, required=True, max_length=50, unique=True)
	pinyin = StringField(max_length=200)
	definitions = ListField(StringField(), default=list)

	def __str__(self):
		return self.hanzi

class Text(Document):
	text = ListField(StringField(), required=True)
	translation = StringField()
	audio = IntField()

	def __str__(self):
		return "".join(self.text)

	def definitions(self):
		list_words = list()
		for word_text in self.text:
			try:
				list_words.append(Word.objects.get(pk=word_text))
			except Word.DoesNotExist:
				pass
		return list_words

	def definitions_to_json(self):
		dict_words = {}
		for word_text in self.text:
			try:
				word = Word.objects.get(pk=word_text)
				dict_words[word.hanzi] = { "pinyin": word.pinyin, "definitions": word.definitions}
			except Word.DoesNotExist:
				pass
		return dict_words



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