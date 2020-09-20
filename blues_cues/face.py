import requests
import json


API_KEY = '385d384953a846119ef795da65630382'
ENDPOINT = 'https://bc-faces.cognitiveservices.azure.com'
filename = '../zoom_gallery_view_test.png'

def make_request(filename, API_KEY, ENDPOINT):
	PATH_TO_API = '/face/v1.0/detect'

	params = {
	    'returnFaceId': 'true',
	    'returnFaceLandmarks': 'false',
	    'returnFaceAttributes': 'age,gender,headPose,smile,emotion',
	}

	headers = {'Ocp-Apim-Subscription-Key': API_KEY, 
			   'Content-Type': 'application/octet-stream'}

	with open(filename, 'rb') as f:
	    img_data = f.read()

	response = requests.post(ENDPOINT + PATH_TO_API, data=img_data, params=params, headers=headers)
	output = response.json()

	return output

def output_analysis(output):

	average_age = 0
	gender = {"male": 0, "female": 0}
	smile = {"Yes": 0, "No": 0}
	num_faces = len(output)
	looking_away = 0

	emotions = []

	for face in output:
		average_age += face['faceAttributes']['age'] / num_faces
		gender[face['faceAttributes']['gender']] += 1
		if face['faceAttributes']['smile'] > 0.5:
			smile["Yes"] += 1
		else:
			smile["No"] += 1

		if abs(face['faceAttributes']['headPose']['pitch']) > 15 or abs(face['faceAttributes']['headPose']['yaw']) > 15:
			looking_away += 1 / num_faces

		emotions.append(face['faceAttributes']['emotion'])

	return round(average_age), gender, smile, looking_away, emotion_analysis(emotions)

def emotion_analysis(emotions):
	total_emotions = {}
	emotion_keys = emotions[0].keys()
	for emotion in emotion_keys:
		total_emotions[emotion] = sum([d[emotion] for d in emotions]) / len(emotions)

	return total_emotions



average_age, gender, smile, looking_away, emotions = output_analysis(make_request(filename, API_KEY, ENDPOINT))
print("Average Age: ", average_age)
print("Gender Distribution: ", gender)
print("Smiles: ", smile)
print("Looking Away (%): ", looking_away*100)
print(emotions)
