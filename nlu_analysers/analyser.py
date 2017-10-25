import urllib
import json
import requests
import time
import sys
from requests.auth import HTTPBasicAuth
from collections import OrderedDict

class Analyser(object):			
	@staticmethod	
	def check_key(my_dict, my_key):
		try:
			t = my_dict[my_key]
		except KeyError:
			my_dict[my_key] = {'truePos': 0, 'falsePos': 0, 'falseNeg': 0}

	@staticmethod
	def try_div(dividend, divisor):
		try:
			return float(dividend) / float(divisor)
		except:
			return "n.a."
	
	@staticmethod
	def sort_dict(my_dict):
		for key in my_dict:
			if isinstance(my_dict[key], dict):
				my_dict[key] = Analyser.sort_dict(my_dict[key])
		
		sort_order = ['intents', 'entities', 'truePos', 'falseNeg', 'falsePos', 'precision', 'recall', 'f1']
		sort_order2 = set(my_dict.keys()) - set(sort_order)		
		my_sort = list(sort_order2)
		my_sort.extend(sort_order)		
		
		return [OrderedDict(sorted(my_dict.iteritems(), key=lambda (k, v): my_sort.index(k)))]
		
	@staticmethod
	def calc_pres_rec_f1(dict, tp, fn, fp):
		dict["precision"] = Analyser.try_div(tp, tp + fp)
		dict["recall"] = Analyser.try_div(tp, tp + fn)
		try:
			dict["f1"] =  2 * ((dict["precision"] * dict["recall"]) / (dict["precision"] + dict["recall"])) 
		except:
			dict["f1"] = "n.a."
			
		return dict
		
	@staticmethod
	def write_json(file, content):
		content = json.loads(content)
		
		#precision, recall, f1	
		os_tp = 0
		os_fn = 0
		os_fp = 0
					
		for x in ["entities", "intents"]:
			s_tp = 0
			s_fn = 0
			s_fp = 0
			
			for key in content[x]:
				s_tp += content[x][key]["truePos"]
				s_fn += content[x][key]["falseNeg"]
				s_fp += content[x][key]["falsePos"]
				
				Analyser.calc_pres_rec_f1(content[x][key], content[x][key]["truePos"], content[x][key]["falseNeg"], content[x][key]["falsePos"])		
							
			os_tp += s_tp
			os_fn += s_fn
			os_fp += s_fp
			
			Analyser.calc_pres_rec_f1(content[x], s_tp, s_fn, s_fp)
		
		Analyser.calc_pres_rec_f1(content, os_tp, os_fn, os_fp)
		
		#sort keys		
		content = Analyser.sort_dict(content)
		
		f = open(file, "w")
		f.write( json.dumps(content, sort_keys=False, indent=4, separators=(',', ': '), ensure_ascii=False).encode('utf-8'))
		f.close()
         
	def __init__(self):
		self.analysis = {}