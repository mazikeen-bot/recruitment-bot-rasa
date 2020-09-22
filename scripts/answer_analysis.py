import requests
import json
from statistics import mean


def answer_score(text):
    data = {"toneInput[text]": text, "contentLanguage": "en"}
    tone_analyser_api = "https://tone-analyzer-demo.ng.bluemix.net/api/tone"
    response = requests.post(url=tone_analyser_api, data=data)
    analysis_result = json.loads(response.text)
    tones_list = analysis_result['document_tone']['tones']
    scores_list = [item['score'] for item in tones_list]
    mean_score = mean(scores_list)
    score_out_of_100 = int(round(mean_score,2) * 100)
    return score_out_of_100
