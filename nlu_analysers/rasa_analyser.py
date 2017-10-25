from luis_analyser import *

class RasaAnalyser(LuisAnalyser):
	def __init__(self, rasa_url):
		super(LuisAnalyser, self).__init__()
		self.url = rasa_url + "?q=%s"