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

	for face in output:
		average_age += face['faceAttributes']['age'] / num_faces
		gender[face['faceAttributes']['gender']] += 1
		if face['faceAttributes']['smile'] > 0.5:
			smile["Yes"] += 1
		else:
			smile["No"] += 1

		if abs(face['faceAttributes']['headPose']['pitch']) > 15 or abs(face['faceAttributes']['headPose']['yaw']) > 15:
			looking_away += 1 / num_faces

	return round(average_age), gender, smile, looking_away


average_age, gender, smile, looking_away = output_analysis(make_request(filename, API_KEY, ENDPOINT))
print("Average Age: ", average_age)
print("Gender Distribution: ", gender)
print("Smiles: ", smile)
print("Looking Away (%): ", looking_away*100)
