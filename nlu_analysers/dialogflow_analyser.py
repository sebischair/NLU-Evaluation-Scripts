from analyser import *

class DialogflowAnalyser(Analyser):
	def __init__(self, api_key):
		super(DialogflowAnalyser, self).__init__()
		self.api_key = api_key
		self.url = "https://api.api.ai/v1/query?v=20170101&sessionId=1234&lang=en&query=%s"
	
	def get_annotations(self, corpus, output):
		data = json.load(open(corpus))		
		annotations = {'results':[]}
		
		for s in data["sentences"]:
			if not s["training"]: #only use test data
				encoded_text = urllib.quote(s['text'])
				headers = { 'Authorization' : 'Bearer %s' %  self.api_key}
				annotations['results'].append(requests.get(self.url % encoded_text,data={},headers=headers).json())
		
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
  			if not a["result"]["resolvedQuery"] == gold_standard[i]["text"]:
  				print "WARNING! Texts not equal"
  			 
  			#intent  			 			
  			try:
  				aIntent = a["result"]["metadata"]["intentName"]
  			except:
  				aIntent = "None"  				
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
  			try:
  				aEntities = a["result"]["metadata"]["entities"]
  			except:
  				aEntities=[]
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