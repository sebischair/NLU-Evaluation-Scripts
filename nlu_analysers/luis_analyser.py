from analyser import *

class LuisAnalyser(Analyser):
	def __init__(self, application_id, subscription_key):
		super(LuisAnalyser, self).__init__()
		self.subscription_key = subscription_key
		self.application_id = application_id
		self.url = "https://westus.api.cognitive.microsoft.com/luis/v2.0/apps/"+self.application_id+"?subscription-key="+self.subscription_key+"&verbose=true&timezoneOffset=0.0&q=%s"
	
	def get_annotations(self, corpus, output):
		data = json.load(open(corpus))		
		annotations = {'results':[]}
		
		for s in data["sentences"]:
			if not s["training"]: #only use test data
				encoded_text = urllib.quote(s['text'])
				annotations['results'].append(requests.get(self.url % encoded_text,data={},headers={}).json())
		
		file = open(output, "w")
  		file.write(json.dumps(annotations, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))
  		file.close()   
  		
  	def analyse_annotations(self, annotations_file, corpus_file, output_file):
  		analysis = {"intents":{}, "entities":{}}  		
  		
  		corpus = json.load(open(corpus_file))
  		gold_standard = []
  		for s in corpus["sentences"]:
			if not s["training"]: #only use test data
				gold_standard.append(s)
  		
  		annotations = json.load(open(annotations_file))
  		
  		i = 0
  		for a in annotations["results"]:
  			if not a["query"] == gold_standard[i]["text"]:
  				print "WARNING! Texts not equal"
  			 
  			#intent  			 			
  			aIntent = a["topScoringIntent"]["intent"]
  			oIntent = gold_standard[i]["intent"]
  			
  			Analyser.check_key(analysis["intents"], aIntent)
  			Analyser.check_key(analysis["intents"], oIntent)
  			
  			if aIntent == oIntent:
  				#correct
  				analysis["intents"][aIntent]["truePos"] += 1
  			else:
  				#incorrect
  				analysis["intents"][aIntent]["falsePos"] += 1
  				analysis["intents"][oIntent]["falseNeg"] += 1
  				
  				
  			#entities
  			aEntities = a["entities"]
  			oEntities = gold_standard[i]["entities"]
  			  			  			
  			for x in aEntities:
  				Analyser.check_key(analysis["entities"], x["type"])
  				
  				if len(oEntities) < 1: #false pos
  					analysis["entities"][x["type"]]["falsePos"] += 1	
  				else:
  					truePos = False
  					
  					for y in oEntities:
  						if x["entity"] == y["text"].lower():
  							if x["type"] == y["entity"]: #truePos
  								truePos = True
  								oEntities.remove(y)
  								break
  							else:						 #falsePos + falseNeg
  								analysis["entities"][x["type"]]["falsePos"] += 1
  								analysis["entities"][y["entity"]]["falseNeg"] += 1
  								oEntities.remove(y)
  								break
  					if truePos:
  						analysis["entities"][x["type"]]["truePos"] += 1
  					else:
  						analysis["entities"][x["type"]]["falsePos"] += 1	
  				
  				
  			for y in oEntities:
  				Analyser.check_key(analysis["entities"], y["entity"])
  				analysis["entities"][y["entity"]]["falseNeg"] += 1	  					
  			  			  				
  			i += 1	
  		
  		self.write_json(output_file, json.dumps(analysis, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))	