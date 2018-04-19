import subprocess
from analyser import *

class DialogflowAnalyser(Analyser):
	def __init__(self, project_id):
		super(DialogflowAnalyser, self).__init__()
		self.url = "https://dialogflow.googleapis.com/v2/projects/" + project_id + "/agent/sessions/1:detectIntent"
	
	def get_annotations(self, corpus, output):
		data = json.load(open(corpus))		
		annotations = {'results':[]}
		
		p = subprocess.Popen(['gcloud', 'auth', 'print-access-token'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		access_token, err = p.communicate()
		access_token = str(access_token).strip()
		for s in data["sentences"]:
			if not s["training"]: #only use test data
				encoded_text = urllib.quote(s['text'])
				headers = {'Authorization':'Bearer %s' %  access_token, 'Content-Type': 'application/json'}
				data = {'queryInput': {'text': {'text': encoded_text, 'languageCode': 'en'}}}
				r = requests.post(self.url, data=json.dumps(data), headers=headers)
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
  		
  		annotations = json.load(open(annotations_file))
  		
  		i = 0
  		for a in annotations["results"]:
  			a = json.loads(a)
  			if not urllib.unquote(a["queryResult"]["queryText"]).decode('utf8') == gold_standard[i]["text"]:
  				print "WARNING! Texts not equal"
  			 
  			#intent  			 			
  			try:
  				aIntent = a["queryResult"]["intent"]["displayName"]
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
  				aEntities = a["queryResult"]["parameters"]
  			except:
  				aEntities = {}
  			oEntities = gold_standard[i]["entities"]
  			  			  			
  			for x in aEntities.keys():
  				Analyser.check_key(analysis["entities"], x)
  				
  				if len(oEntities) < 1: #false pos
  					analysis["entities"][x]["falsePos"] += 1
  				else:
  					truePos = False
  					
  					for y in oEntities:
  						if len(aEntities[x]) != 0 and aEntities[x][0].lower() == y["text"].lower():
  							if x == y["entity"]: #truePos
  								truePos = True
  								oEntities.remove(y)
  								break
  							else:						 #falsePos + falseNeg
  								analysis["entities"][x]["falsePos"] += 1
  								analysis["entities"][y["entity"]]["falseNeg"] += 1
  								oEntities.remove(y)
  								break
  					if truePos:
  						analysis["entities"][x]["truePos"] += 1
  					else:
  						analysis["entities"][x]["falsePos"] += 1

  			for y in oEntities:
  				Analyser.check_key(analysis["entities"], y["entity"])
  				analysis["entities"][y["entity"]]["falseNeg"] += 1	  					
  			  			  				
  			i += 1	
  		
  		self.write_json(output_file, json.dumps(analysis, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))	
