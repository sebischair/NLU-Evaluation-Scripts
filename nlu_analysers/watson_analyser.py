from analyser import *

class WatsonAnalyser(Analyser):
	def __init__(self, workspace_id, user, password):
		super(WatsonAnalyser, self).__init__()
		self.workspace_id = workspace_id
		self.user = user
		self.password = password
		self.url = "https://gateway.watsonplatform.net/assistant/api/v1/workspaces/" + self.workspace_id + "/message?version=2018-02-16"
		
	
	def get_annotations(self, corpus, output):
		data = json.load(open(corpus))		
		annotations = {'results':[]}
		
		for s in data["sentences"]:
			if not s["training"]: #only use test data
				encoded_text = urllib.quote(s['text'])
				headers = {'content-type': 'application/json'}
				data = {"input":{"text":encoded_text}}
				r = requests.post(self.url, data=json.dumps(data), headers=headers, auth=(self.user, self.password))
				annotations['results'].append(r.text)
		
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
  		
  		#print urllib.unquote(open(annotations_file).read()).decode('utf8') 
  		annotations = json.load(open(annotations_file))
  		
  		i = 0
  		for a in annotations["results"]:
  			a = json.loads(a)
  			if not urllib.unquote(a["input"]["text"]).decode('utf8') == gold_standard[i]["text"]:
  				print "WARNING! Texts not equal"
  			 
  			#intent  			 			
			if (len(a["intents"]) > 0):
				aIntent = a["intents"][0]["intent"]
			else:
				aIntent = None
  			oIntent = gold_standard[i]["intent"].replace(" ", "_")
  			
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
  				Analyser.check_key(analysis["entities"], x["entity"])
  				
  				if len(oEntities) < 1: #false pos
  					analysis["entities"][x["entity"]]["falsePos"] += 1	
  				else:
  					truePos = False
  					
  					for y in oEntities:
  						if x["value"] == y["text"].lower():
  							if x["entity"] == y["entity"]: #truePos
  								truePos = True
  								oEntities.remove(y)
  								break
  							else:						 #falsePos + falseNeg
  								analysis["entities"][x["entity"]]["falsePos"] += 1
  								analysis["entities"][y["entity"]]["falseNeg"] += 1
  								oEntities.remove(y)
  								break
  					if truePos:
  						analysis["entities"][x["entity"]]["truePos"] += 1
  					else:
  						analysis["entities"][x["entity"]]["falsePos"] += 1	
  				
  				
  			for y in oEntities:
  				Analyser.check_key(analysis["entities"], y["entity"])
  				analysis["entities"][y["entity"]]["falseNeg"] += 1	  					
  			  			  				
  			i += 1	
  		
  		self.write_json(output_file, json.dumps(analysis, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))	