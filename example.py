from nlu_converters.luis_converter import LuisConverter

#convert training data

#luis
luis_converter = LuisConverter()
luis_converter.import_corpus("WebApplicationsCorpus.json")
luis_converter.export("WebApplicationsTraining_LUIS.json")