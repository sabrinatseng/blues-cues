from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, KeywordsOptions
import json
from os.path import join, dirname



def authenticate(API_KEY, f, url, version=None):
	authenticator = IAMAuthenticator(API_KEY)
	if version:
		service = f(version=version, authenticator=authenticator)
	else:
		service = f(authenticator=authenticator)
	service.set_service_url(url)
	return service

def speech_to_text(audio):
	API_KEY = 'a1-eB6G1QxqycOi54Rfc0vWglp_0IhVrs6g5crQg0nIu'
	url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/d6a2a513-b0db-4a1f-9d90-be446806e7fd'
	speech_to_text = authenticate(API_KEY, SpeechToTextV1, url)
	
	with open(audio, 'rb') as audio_file:
		return speech_to_text.recognize(
	            audio=audio_file,
	            content_type='audio/wav',
	            timestamps=True,
	            word_confidence=True).get_result()

def extract_text(audio):
	json_output = speech_to_text(audio)
	text = ""
	for segment in json_output['results']:
		text += segment['alternatives'][0]['transcript']
	print(text)
	return text

def keywords(text):
	API_KEY = 'b6NOltM3-zpJPqI4KiGfhfHLM6fkSkJMUKHKlBvOSn4G'
	url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/62ddc339-68c4-414a-b6da-bf78870c170f'
	nlu = authenticate(API_KEY, NaturalLanguageUnderstandingV1, url, version='2020-08-01')

	analysis = nlu.analyze(text=text, features=Features(
        concepts=ConceptsOptions(limit=5),
        keywords=KeywordsOptions(emotion=True, sentiment=True,
                                 limit=5))).get_result()

	return analysis


def sentiment(text):
	API_KEY = 'cLAHEJMYhkYcLe-DspAYCQeffiAtXoX0owOFQ_JPy52w'
	url = 'https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/b15a9c0c-c0eb-4212-8dfc-3f25074909be'
	tone_analyzer = authenticate(API_KEY, ToneAnalyzerV3, url, version='2017-09-21')

	tone_analysis = tone_analyzer.tone(
	    {'text': text},
	    content_type='application/json'
	).get_result()
	return tone_analysis

print(keywords(extract_text("output.wav")))




