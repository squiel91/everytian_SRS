from django.http import JsonResponse, HttpResponse
from ..models import Text, User, Knowledge, Word
from random import randint
from collections import defaultdict

import pdb

# punctuation = u'…！？／（）、，。：「」…『』！？《》“”；’ ‘【】·〔〕.,?!-[]'

# def select_next(user):
	# actual = None
	# max_known_words = 0
	# best_sentence = None
	# for text in Text.objects.all():
	# 	known_words = 0
	# 	unknown_words = 0
	# 	undefined = 0
	# 	actual = text
	# 	for word in actual.text:
	# 		if word not in punctuation:
	# 			try:
	# 				# pdb.set_trace()
	# 				knowledge = Knowledge.objects.get(user=user, word=word)
	# 				if knowledge.known:
	# 					known_words += 1
	# 				else:
	# 					unknown_words += 1
	# 			except Knowledge.DoesNotExist:
	# 				undefined += 1
	# 	# if text.audio ==333219:
	# 	# 	pdb.set_trace()
	# 	if max_known_words <= known_words and unknown_words + undefined <= 2 and text not in user.resource_history:
	# 		max_known_words = known_words
	# 		best_sentence = text

	# # return best_sentence

def update_knowledge(user, resource_id, unknown_word_ids):
	feedback = defaultdict(list)

	resource = Text.objects.get(pk=resource_id)
	all_words = set(resource.text)
	unknown_words = set(unknown_word_ids)

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
	user.save()

	return feedback

def next_recommendation():
	position = randint(1, Text.objects.count()) - 1
	return Text.objects.all()[position]

def resources(request, id):
	# pdb.set_trace()
	if not request.session.get('email'):
		return JsonResponse({"error": "Bad authentication"}, status=401)
	user = User.objects.get(pk=request.session['email'])

	if request.method == "GET":
		response_json = {}
		if "resource_id" in request.GET:
			if request.POST.get("favorite") == "on":
				user.add_favorite(resource)
				user.save()
			response_json.update(update_knowledge(
				user, 
				request.GET["resource_id"], 
				request.POST.getlist("unknown_words[]"))
			)

		resource = None
		if id:
			resource = Text.objects.get(pk=id)
		else:
			resource = next_recommendation()
		response_json.update(resource.serialize())
		return JsonResponse(response_json)
	
	if request.method == "POST":
		if id:
			resource = Text.objects.get(pk=id)
			resource.text = request.POST.getlist("text[]")
			resource.translation = request.POST["translation"]
			resource.save()
			return JsonResponse(resource.serialize())
		else:
			HttpResponse("A new resource will be created")
