# Blue's Cues
Augmenting the video-conferencing experience with real-time analytics on audience engagement and social cues to foster more natural conversations

Communication in the COVID era is hard; advancements in video-conferencing are no match for the social cues that we humans use to navigate in-person conversations. **Blue's Cues** aims to bridge this gap and enhance the video-conferencing experience by offering users real-time data audience sentiment, engagement, and behaviors.

## Setup
Make sure to install `portaudio`, which is a dependency for `pyaudio`. You can install all of the project dependencies from `requirements.txt`:
```
# Mac installation
$ brew install portaudio
$ pip install -r requirements.txt
```

To run:
```
$ python3 main.py
```
Note: you may need to allow your terminal to record your screen so that we can screencapture your Zoom window and provide insights.

## Built With
* Python
* Tkinter for the display panel
* IBM-Watson (Speech-to-Text, Natural Language Understanding) for audio analysis
* Microsoft Azure (Cognitive Services - Face) for facial recognition and analysis
* OpenCV for visual analysis of the Zoom view
