from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..models import User, Word, Text, Knowledge, EvolutionRecord
from random import randint
import pdb
import sys
from collections import defaultdict

class WordTemplate:

	def __init__(self, hanzi, pinyin):
		self.hanzi = hanzi
		self.pinyin = pinyin

def text_with_def(text, word_definitions):
	list_words_pinyin = []
	for word in text:
		if word in word_definitions:
			list_words_pinyin.append(WordTemplate(word, word_definitions[word]["pinyin"]))
		else:
			list_words_pinyin.append(WordTemplate(word, ""))
	return list_words_pinyin

def get_view_dict(resource):
	word_definitions = resource.definitions_to_json()
	return {
		"resource_id": resource.id,
		"text": text_with_def(resource.text, word_definitions),
		"tweet": "".join(resource.text),
		"word_definitions": word_definitions,
		"translation": resource.translation,
		"audio": resource.audio,
	}

punctuation = u'…！？／（）、，。：「」…『』！？《》“”；’ ‘【】·〔〕.,?!-[]'

def select_next(user):
	actual = None
	max_known_words = 0
	best_sentence = None
	for text in Text.objects.all():
		known_words = 0
		unknown_words = 0
		undefined = 0
		actual = text
		for word in actual.text:
			if word not in punctuation:
				try:
					# pdb.set_trace()
					knowledge = Knowledge.objects.get(user=user, word=word)
					if knowledge.known:
						known_words += 1
					else:
						unknown_words += 1
				except Knowledge.DoesNotExist:
					undefined += 1
		# if text.audio ==333219:
		# 	pdb.set_trace()
		if max_known_words <= known_words and unknown_words + undefined <= 2 and text not in user.resource_history:
			max_known_words = known_words
			best_sentence = text
	
	# position = randint(1, Text.objects.count()) - 1
	# return Text.objects.all()[position]
	return best_sentence


def practice(request):
	# ¡¡pdb.set_trace()
	if not request.session.get('email'):
		return redirect('login')
	user = User.objects.get(pk=request.session['email'])

	feedback = defaultdict(list)

	if request.method == "POST":
		# pdb.set_trace()
		resource = Text.objects.get(pk=request.POST["resource_id"])
		all_words = set(resource.text)
		unknown_words = set(request.POST.getlist("unknown"))
		
		for word_str in all_words:
			try:
				word = Word.objects.get(pk=word_str)
				known = word_str not in unknown_words
				try:
					kng = Knowledge.objects.get(word=word, user=user)
					word_feedback = kng.update_status(known)
					feedback[word_feedback].append(word_str)
				except Knowledge.DoesNotExist:
					Knowledge.objects.create(word=word, user=user, known=known)
					if known:
						feedback["discov_known"].append(word_str)
					else:
						feedback["discov_unknown"].append(word_str)
			except Word.DoesNotExist:
				pass
				
		user.add_history(resource, learned=feedback["learned"], forgotten=feedback["forgotten"],
			discov_known=feedback["discov_known"], discov_unknown=feedback["discov_unknown"])
		if request.POST.get("favorite") == "on":
			user.add_favorite(resource)
		user.save()

	text = select_next(user)
	view_dict = get_view_dict(text)
	view_dict["learned"] = feedback["learned"]
	view_dict["forgotten"] = feedback["forgotten"]
	view_dict["discov_known"] = feedback["discov_known"]
	view_dict["discov_unknown"] = feedback["discov_unknown"]

	return render(request, 'practice.html', view_dict)
