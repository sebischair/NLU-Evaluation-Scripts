# NLU-Evaluation-Scripts
Python scripts for automatically evaluating NLU services (API.ai, IBM Watson Conversation, Microsoft LUIS, RASA) based on the format used by [NLU-Evaluation-Corpora](https://github.com/sebischair/NLU-Evaluation-Corpora).

## Training
You can use the coverters to create .json-files with training data which can be imported into the respective NLU service.
```python
#luis
luis_converter = LuisConverter()
luis_converter.import_corpus("WebApplicationsCorpus.json")
luis_converter.export("WebApplicationsTraining_LUIS.json")
```
