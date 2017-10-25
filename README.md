# NLU-Evaluation-Scripts
Python scripts for automatically evaluating NLU services (API.ai, IBM Watson Conversation, Microsoft LUIS, RASA) based on the format used by [NLU-Evaluation-Corpora](https://github.com/sebischair/NLU-Evaluation-Corpora).

## Training
You can use the converters to create .json- or .zip-files with training data which can be imported into the respective NLU service using the web interface.

### Microsoft Luis
```python
#luis (also works for rasa)
luis_converter = LuisConverter()
luis_converter.import_corpus("WebApplicationsCorpus.json")
luis_converter.export("WebApplicationsTraining_Luis.json")
```
You can also use the Luis file format to train Rasa, however, we recommend using the Dialogflow data format for training Rasa.

### IBM Watson Conversation
```python
#watson
watson_converter = WatsonConverter()
watson_converter.import_corpus("WebApplicationsCorpus.json")
watson_converter.export("WebApplicationsTraining_Watson.json")
```
### Dialogflow (formerly known as API.ai)
```python
#dialogflow (also works for rasa)
dialogflow_converter = DialogflowConverter()
dialogflow_converter.import_corpus("WebApplicationsCorpus.json")
dialogflow_converter.export("WebApplicationsTraining_Dialogflow.zip")
```

## Evaluation
You can use the analysers to annotate the test data and generate a .json-file with an evaluation of the annotations.

### Microsoft Luis
```python
#luis
luis_analyser = LuisAnalyser("application_id", "subscription_key")
luis_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Luis.json")
luis_analyser.analyse_annotations("WebApplicationsAnnotations_Luis.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Luis.json")
```
### IBM Watson Conversation
```python
#watson
watson_analyser = WatsonAnalyser("workspace_id", "user", "password")
watson_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Watson.json")
watson_analyser.analyse_annotations("WebApplicationsAnnotations_Watson.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Watson.json")
```
### Dialogflow (formerly known as API.ai)
```python
#dialogflow
dialogflow_analyser = DialogflowAnalyser("api_key")
dialogflow_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Dialogflow.json")
dialogflow_analyser.analyse_annotations("WebApplicationsAnnotations_Dialogflow.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Dialogflow.json")
```

### Rasa NLU
In order to evaluate the annotations from Rasa, you have to start the Rasa server with the option "-e luis".
```python
#rasa
rasa_analyser = RasaAnalyser("http://localhost:5000/parse")
rasa_analyser.get_annotations("WebApplicationsCorpus.json", "WebApplicationsAnnotations_Rasa.json")
rasa_analyser.analyse_annotations("WebApplicationsAnnotations_Rasa.json", "WebApplicationsCorpus.json", "WebApplicationsAnalysis_Rasa.json")
```

## Contact Information
If you have any questions, please contact:

[Daniel Braun](https://wwwmatthes.in.tum.de/pages/41usp76zyc49/Daniel-Braun) (Technical University of Munich) daniel.braun@tum.de
