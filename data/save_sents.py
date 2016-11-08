from web.models import Text
import json

texts = json.load(open('data/chinese_sentences.json'))

for text in texts:
	if len(text["translations"]) > 0 and text["audio"]:
		Text.objects.create(
			text=text["sentence"],
			audio=text["tatoeba_id"] if text["audio"] else 0,
			translation=text["translations"][0]
		)