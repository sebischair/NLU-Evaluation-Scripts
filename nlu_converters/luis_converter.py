from converter import *

class LuisConverter(Converter):
	LUIS_SCHEMA_VERSION = "1.3.0"
			
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
			entities.append({"entity":e["entity"],"startPos":e["start"],"endPos":e["stop"]})
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
		luis_json["name"] = self.name
		luis_json["desc"] = self.desc
		luis_json["culture"] = self.lang  
		luis_json["intents"] = self.array_to_json(self.intents)
		luis_json["entities"] = self.array_to_json(self.entities)
		luis_json["bing_entities"] = self.array_to_json(self.bing_entities)
		luis_json["actions"] = []
		luis_json["model_features"] = []
		luis_json["regex_features"] = []
		luis_json["utterances"] = self.utterances

		self.write_json(file, luis_json)