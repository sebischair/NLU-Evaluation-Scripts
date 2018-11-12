from nlu_converters.luis_converter import LuisConverter
from nlu_converters.watson_converter import WatsonConverter
from nlu_converters.dialogflow_converter import DialogflowConverter

from nlu_analysers.luis_analyser import LuisAnalyser
from nlu_analysers.watson_analyser import WatsonAnalyser
from nlu_analysers.dialogflow_analyser import DialogflowAnalyser
from nlu_analysers.rasa_analyser import RasaAnalyser

#convert training data
##luis (also works for rasa)
luis_converter = LuisConverter()
luis_converter.import_corpus("WebApplicationsCorpus.json")
luis_converter.export("WebApplicationsTraining_Luis.json")

##watson
watson_converter = WatsonConverter()
watson_converter.import_corpus("WebApplicationsCorpus.json")
watson_converter.export("WebApplicationsTraining_Watson.json")

##dialogflow (also works for rasa)
dialogflow_converter = DialogflowConverter()
dialogflow_converter.import_corpus("WebApplicationsCorpus.json")
dialogflow_converter.export("WebApplicationsTraining_Dialogflow.zip")


#test nlu services
##luis
luis_analyser = LuisAnalyser("application_id", "subscription_key")
luis_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Luis.json")
luis_analyser.analyse_annotations("WebApplicationsAnnotations_Luis.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Luis.json")

##watson
watson_analyser = WatsonAnalyser("workspace_id", "user", "password")
watson_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Watson.json")
watson_analyser.analyse_annotations("WebApplicationsAnnotations_Watson.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Watson.json")

##dialogflow
dialogflow_analyser = DialogflowAnalyser("project_id")
dialogflow_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Dialogflow.json")
dialogflow_analyser.analyse_annotations("WebApplicationsAnnotations_Dialogflow.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Dialogflow.json")

##rasa
rasa_analyser = RasaAnalyser("http://localhost:5000/parse")
rasa_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Rasa.json")
rasa_analyser.analyse_annotations("WebApplicationsAnnotations_Rasa.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Rasa.json")
