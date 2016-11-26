

def serialize(text):
	serialized = {}
	serialized["text"] = text.text
	serialized["translation"] = text.translation
	serialized["audio"] = text.audio
	serialized["words"] = [word.serialize() for word in text.definitions()]
	return serialized

def deserialize(text):
	serialized = {}
	serialized["text"] = text.text
	serialized["translation"] = text.translation
	serialized["audio"] = text.audio
	serialized["words"] = [word.serialize() for word in text.definitions()]
	return serialized

def update(text):
	serialized = {}
	serialized["text"] = text.text
	serialized["translation"] = text.translation
	serialized["audio"] = text.audio
	serialized["words"] = [word.serialize() for word in text.definitions()]
	return serialized