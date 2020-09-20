from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1, ToneAnalyzerV3, NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, KeywordsOptions
from ibm_cloud_sdk_core.api_exception import ApiException
import json
from os.path import join, dirname
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "output.wav"
UPDATE_TIME_SECS = 2


class AudioProcessor():

	def __init__(self):
		pass
	def record_audio(self):
		frames = []
		p = pyaudio.PyAudio()
		SPEAKERS = p.get_default_output_device_info()["hostApi"]
		
		stream = p.open(format=FORMAT,
		                channels=CHANNELS,
		                rate=RATE,
		                input=True,
		                frames_per_buffer=CHUNK,
		                input_host_api_specific_stream_info=SPEAKERS)

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
		    data = stream.read(CHUNK)
		    frames.append(data)

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()

	def authenticate(self, API_KEY, f, url, version=None):
		authenticator = IAMAuthenticator(API_KEY)
		if version:
			service = f(version=version, authenticator=authenticator)
		else:
			service = f(authenticator=authenticator)
		service.set_service_url(url)
		return service

	def speech_to_text(self, audio):
		API_KEY = 'a1-eB6G1QxqycOi54Rfc0vWglp_0IhVrs6g5crQg0nIu'
		url = 'https://api.us-east.speech-to-text.watson.cloud.ibm.com/instances/d6a2a513-b0db-4a1f-9d90-be446806e7fd'
		speech_to_text = self.authenticate(API_KEY, SpeechToTextV1, url)
		
		with open(audio, 'rb') as audio_file:
			return speech_to_text.recognize(
		            audio=audio_file,
		            content_type='audio/wav',
		            timestamps=True,
		            word_confidence=True).get_result()


	def extract_text(self, audio):
		json_output = self.speech_to_text(audio)
		text = ""
		for segment in json_output['results']:
			text += segment['alternatives'][0]['transcript']
		print(text)
		return text

	def keywords(self, text):
		API_KEY = 'b6NOltM3-zpJPqI4KiGfhfHLM6fkSkJMUKHKlBvOSn4G'
		url = 'https://api.us-east.natural-language-understanding.watson.cloud.ibm.com/instances/62ddc339-68c4-414a-b6da-bf78870c170f'
		nlu = self.authenticate(API_KEY, NaturalLanguageUnderstandingV1, url, version='2020-08-01')

		analysis = nlu.analyze(text=text, features=Features(
	        concepts=ConceptsOptions(limit=5),
	        keywords=KeywordsOptions(emotion=True, sentiment=True,
	                                 limit=5))).get_result()

		return analysis


	def sentiment(self, text):
		API_KEY = 'cLAHEJMYhkYcLe-DspAYCQeffiAtXoX0owOFQ_JPy52w'
		url = 'https://api.us-east.tone-analyzer.watson.cloud.ibm.com/instances/b15a9c0c-c0eb-4212-8dfc-3f25074909be'
		tone_analyzer = self.authenticate(API_KEY, ToneAnalyzerV3, url, version='2017-09-21')

		tone_analysis = tone_analyzer.tone(
		    {'text': text},
		    content_type='application/json'
		).get_result()
		return tone_analysis

	def format_keywords(self, output):
		num_words = min(2, len(output['keywords']))
		content = ""
		for n in range(num_words):
			content += output['keywords'][n]['text'] + ", "

		return content[:-2]

	def format_sentiment(self, output):
		num_words = min(2, len(output['document_tone']['tones']))
		content = ""
		for n in range(num_words):
			content += output['document_tone']['tones'][n]['tone_id'] + ", "

		return content[:-2]


	def run(self, queue):
		while True:
			print("audio processor iteration")
			self.record_audio()
			try: 
				text = self.extract_text(WAVE_OUTPUT_FILENAME)
				kws = self.format_keywords(self.keywords(text))
				tone_id = self.format_sentiment(self.sentiment(text))

				title = "Speech Analysis"
				content = "Tone: {}\nKeywords: {}".format(tone_id, kws)
				queue.put((title, content))

			except:
				print("Silence")

