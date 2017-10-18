import urllib
import json
import requests
import time
import sys
from requests.auth import HTTPBasicAuth

class Analyser(object):			
	@staticmethod	
	def check_key(my_dict, my_key):
		try:
			t = my_dict[my_key]
		except KeyError:
			my_dict[my_key] = {'truePos': 0, 'falsePos': 0, 'falseNeg': 0}
    
	@staticmethod
	def write_json(file, content):
		f = open(file, "w")
		f.write(content)
		f.close()
         
	def __init__(self):
		self.analysis = {}