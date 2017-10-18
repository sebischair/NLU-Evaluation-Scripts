from nlu_converters.luis_converter import LuisConverter
#from nlu_converters.ibm_converter import IBMConverter

from nlu_analysers.luis_analyser import LuisAnalyser

#convert training data
##luis
luis_converter = LuisConverter()
luis_converter.import_corpus("WebApplicationsCorpus.json")
luis_converter.export("WebApplicationsTraining_LUIS.json")

##watson
#ibm_converter = IBMConverter()
#ibm_converter.import_corpus("WebApplicationsCorpus.json")
#ibm_converter.export("WebApplicationsTraining_Watson.json")


#test nlu services
##luis
luis_analyser = LuisAnalyser("ASDF", "GHI")
luis_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_LUIS.json")
luis_analyser.analyse_annotations("WebApplicationsAnnotations_LUIS.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_LUIS.json")