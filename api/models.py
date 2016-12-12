from django.db import models
from mongoengine import *
import datetime
import json

pronunciations = ('tonal', 'numeric', 'bopomofo')

class Word(Document):
	hanzi = StringField(primary_key=True, required=True, max_length=50, unique=True)
	pinyin = StringField(max_length=200)
	definitions = ListField(StringField(), default=list)
	composed_by = ListField(StringField(), default=list)

	def __str__(self):
		return self.hanzi

	def composed_by_definitions(self):
		list_words = list()
		for word_text in self.composed_by:
			try:
				list_words.append(Word.objects.get(pk=word_text).serialize())
			except Word.DoesNotExist:
				pass
		return list_words

	def serialize(self):
		if self.pinyin:
			serialized = {}
			serialized["hanzi"] = self.hanzi
			serialized["pinyin"] = self.pinyin
			serialized["definitions"] = self.definitions
			serialized["composed_by"] = self.composed_by_definitions()
			return serialized
		return None

class Answer(EmbeddedDocument):
	user_email =  StringField(required=True)
	text = StringField(required=True)

	def serialize(self):
		serialized = {}
		serialized["user_email"] = self.user_email
		serialized["text"] = self.text
		return serialized

class Question(EmbeddedDocument):
	user_email = StringField(required=True)
	text = StringField(required=True)
	answers = ListField(EmbeddedDocumentField(Answer), default=list)

	def serialize(self):
		serialized = {}
		serialized["user_email"] = self.user_email
		serialized["text"] = self.text
		serialized["answers"] = [a.serialize() for a in self.answers]
		return serialized


class Text(Document):
	text = ListField(StringField(), required=True)
	translation = StringField()
	audio = IntField()
	questions = ListField(EmbeddedDocumentField(Question), default=list)

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

	def serialize(self):
		serialized = {}
		serialized["id"] = str(self.id)
		serialized["text"] = self.text
		serialized["translation"] = self.translation
		serialized["audio"] = self.audio
		serialized["words"] = [word.serialize() for word in self.definitions()]
		serialized["questions"] = [question.serialize() for question in self.questions]
		return serialized

	def update(self):
		# doesnt update questions nor answers
		serialized = {}
		serialized["text"] = self.text
		serialized["translation"] = self.translation
		serialized["audio"] = self.audio
		serialized["words"] = [word.serialize() for word in self.definitions()]
		return serialized

class EvolutionRecord(EmbeddedDocument):
	text_number = IntField(primary_key=True)
	known_words = IntField()
	unknown_words = IntField()
	discov_known = IntField()
	discov_unknown = IntField()
	learned = IntField()
	forgotten =  IntField()
	date =  DateTimeField(default=datetime.datetime.now)

	def get_known_unknown(self):
		return [self.text_number, self.known_words, self.unknown_words]

	def get_dicov_known_unknown(self):
		return [self.text_number, self.discov_known, self.discov_unknown]

	def get_learn_forgotten(self):
		return [self.text_number, self.learned, self.forgotten]

class User(Document):
	email = EmailField(max_length=100, required=True, primary_key=True, unique=True)
	name = StringField(max_length=25, required=True)
	password = StringField(max_length=100)
	simplified = BooleanField()
	pronunciation = StringField(max_length=20, choices=pronunciations)
	verified_email = BooleanField(default=False)
	verify_email_token = IntField(default=1234)

	resource_history = ListField(ReferenceField(Text))
	favorite_resources = ListField(ReferenceField(Text))

	history = ListField(EmbeddedDocumentField(EvolutionRecord), default=lambda:[EvolutionRecord(
			text_number = 0,
			known_words = 0,
			unknown_words = 0,
			discov_known = 0,
			discov_unknown = 0,
			learned = 0,
			forgotten = 0
		)])
	
	def add_favorite(self, resource):
		self.favorite_resources.append(resource)
		self.save()

	def add_history(self, resource, learned=None, forgotten=None,
		discov_known=None, discov_unknown=None):
		if resource and learned and forgotten and discov_known and discov_unknown:
			raise Exception('add_history method needs all arguments instanciated')
		last_record = self.history[-1]
		new_record = EvolutionRecord(
			text_number=last_record.text_number + 1,
			known_words=last_record.known_words + len(discov_known) - len(forgotten) + len(learned), 
			unknown_words=last_record.unknown_words + len(discov_unknown) + len(forgotten) - len(learned),
			forgotten =last_record.forgotten + len(forgotten),
			learned = last_record.learned + len(learned),
			discov_known =last_record.discov_known + len(discov_known), 
			discov_unknown =last_record.discov_unknown + len(discov_unknown), 
		)
		self.history.append(new_record)
		self.resource_history.append(resource)
		self.save()

	def __str__(self):
		return "".join(self.email)

class Knowledge(Document):
	user = ReferenceField(User)
	word =  ReferenceField(Word)
	known = BooleanField()
	
	def __str__(self):
		state = "knowns" if self.known else "unknowns"
		return "{} {} {}".format(user, state, word)

	def update_status(self, known):
		updated = None
		if self.known:
			if known:
				updated = "known"
			else:
				updated = "forgotten"
		else:
			if known:
				updated = "learned"
			else:
				updated = "unknown"
		self.known = known
		self.save()
		return updated
