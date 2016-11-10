from web.models import Word
import json

words = json.load(open('data/cedict_new.json'))

for word in words:
	Word.objects.create(
		hanzi=word["word"]["traditional"],
		pinyin=word["pinyin"],
		definitions=word["definitions"]
	)