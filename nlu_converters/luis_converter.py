from converter import *

class LuisConverter(Converter):
	LUIS_SCHEMA_VERSION = "2.2.0"

	def __init__(self):
		super(LuisConverter, self).__init__()
		self.bing_entities = set()

	def __add_intent(self, intent):
		self.intents.add(intent)

	def __add_entity(self, entity):
		self.entities.add(entity)

	def __add_bing_entity(self, entity):
		self.bing_entities.add(entity)

	def __add_utterance(self, sentence):
		entities = []
		for e in sentence.entities:
			#Calculate the position based on character count.
			words = (sentence.text).split(' ')
			index = 0
			for i in range(len(words)):
				if i == e["start"]:
					start_index = index
					end_index = index + len(words[i])
				elif i == e["stop"]:
					end_index = index + len(words[i])
					break
				index = index + len(words[i]) + 1
			#print start_index, end_index
			entities.append({"entity": e["entity"], "startPos": start_index, "endPos": end_index-1})
		self.utterances.append({"text": sentence.text, "intent": sentence.intent, "entities": entities})

	def import_corpus(self, file):
		data = json.load(open(file))
		#meta data
		self.name = data["name"]
		self.desc = data["desc"]
		#dirty quickfix
		if(data["lang"] == "en"):
			self.lang = "en-us"
		else:
			self.lang = data["lang"] + "-" + data["lang"]

		#training data
		for s in data["sentences"]:
			if s["training"]: #only import training data
				#intents
				self.__add_intent(s["intent"])			
				#entities
				for e in s["entities"]:				
					self.__add_entity(e["entity"])        	
				#utterances
				self.__add_utterance(AnnotatedSentence(s["text"], s["intent"], s["entities"]))

	def export(self, file):
		luis_json = {}
		luis_json["luis_schema_version"] = self.LUIS_SCHEMA_VERSION 
		luis_json["versionId"] = "0.1.0"
		luis_json["name"] = self.name
		luis_json["desc"] = self.desc
		luis_json["culture"] = self.lang  
		luis_json["intents"] = self.array_to_json(self.intents)
		luis_json["entities"] = self.array_to_json(self.entities)
		luis_json["bing_entities"] = self.array_to_json(self.bing_entities)
		luis_json["model_features"] = []
		luis_json["regex_features"] = []
		luis_json["regex_entities"] = []
		luis_json["composites"] = []
		luis_json["closedLists"] = []
		luis_json["utterances"] = self.utterances
		json_data = json.dumps(luis_json, indent=4, sort_keys=True)
		self.write_json(file, json_data)
