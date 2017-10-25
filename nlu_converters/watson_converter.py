from converter import *
import datetime

class WatsonConverter(Converter):			
	def __init__(self):
		super(WatsonConverter, self).__init__()
		self.workspace_id = ""
		self.entities = [] #overwrite set with array
			
	
	def __add_intents(self, intent, sentence):
		intent = intent.replace(" ", "_")
		
		date = datetime.datetime.utcnow().isoformat() + 'Z'
		for i in self.utterances:
			if i["intent"] == intent: #add utterance to existing intent
				i["examples"].append({"text": sentence, "created": date, "updated": date})
				return
		#add new intent
		i = {"intent": intent, "created": date, "updated": date, "examples": [], "description": None}
		i["examples"].append({"text": sentence, "created": date, "updated": date})
		self.utterances.append(i)
				
	def __add_entity(self, sentence):
		date = datetime.datetime.utcnow().isoformat() + 'Z'
		s = Converter.tokenizer(sentence.text)
		value = ""
		
		for e in self.entities:
			if e["entity"] == sentence.entities["entity"]:				
				for i in range(int(sentence.entities["start"]), int(sentence.entities["stop"])+1):
					value = value + s[i] + " "
					value = Converter.detokenizer(value)
				for x in e["values"]:
					if x["value"] == value.rstrip().lower():
						return
				e["values"].append({"value": value.rstrip().lower(), "created": date, "updated": date, "metadata":None, "synonyms":[]})
				return
					
		e = {"type": None, "source": None, "created": date, "updated": date, "open_list": False, "description": None, "entity": sentence.entities["entity"], "values": []}
		for i in range(int(sentence.entities["start"]), int(sentence.entities["stop"])+1):
			value = value + s[i] + " "
			value = Converter.detokenizer(value)
		e["values"].append({"value": value.rstrip().lower(), "created": date, "updated": date, "metadata":None, "synonyms":[]})

		self.entities.append(e)
	
		
	def import_corpus(self, file):
		data = json.load(open(file))
		
		#meta data
		self.name = data["name"]
		self.desc = data["desc"]
		self.lang = data["lang"]
		
		#training data
		for s in data["sentences"]:
			if s["training"]: #only import training data
				#intents and utterances
				self.__add_intents(s["intent"], s["text"])
				#entities
				for e in s["entities"]:
					self.__add_entity(AnnotatedSentence(s["text"], s["intent"], e))

	def export(self, file):
		watson_json = {}
		watson_json["name"] = self.name
		watson_json["description"] = self.desc
		watson_json["language"] = self.lang  
		watson_json["metadata"] = None
		watson_json["counterexamples"] = []
		watson_json["dialog_nodes"] = [] 
		watson_json["created"] = datetime.datetime.utcnow().isoformat() + 'Z'
		watson_json["updated"] = datetime.datetime.utcnow().isoformat() + 'Z'
		watson_json["workspace_id"] = self.workspace_id 
		watson_json["intents"] = self.utterances 
		watson_json["entities"] = self.entities 

		self.write_json(file, json.dumps(watson_json, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))