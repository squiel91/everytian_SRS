from django.http import JsonResponse
from ..models import Word
import pdb

def words(request, id):
	# pdb.set_trace()
	if request.method == "GET":
		if id:
			try:
				word = Word.objects.get(pk=id)
				return JsonResponse(word.serialize())
			except Word.DoesNotExist:
				return JsonResponse({"warning": "{} is not in the dictionary".format(id)})
		else:
			pass
	return JsonResponse(id)

# def words(request, ids):
# 	# pdb.set_trace()
# 	if request.method == "GET":
# 		if ids:
# 			ids = ids.split(',')
# 			words = []
# 			for id in ids:
# 				try:
# 					words.append(Word.objects.get(pk=id))
# 				except Word.DoesNotExist:
# 					pass
# 			# pdb.set_trace()
# 			return JsonResponse([word.serialize() for word in words], safe=False)
# 		else:
# 			pass
# 	return JsonResponse(id)