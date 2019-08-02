import json, sys

obs_to_sent_and_cat = 'res/obs_to_sent_and_cat.json'
reading_examples = 'res/reading_examples.json'

with open(obs_to_sent_and_cat) as f:
	obs_to_sent_and_cat = json.load(f)

with open(obs_to_sent_and_cat) as f:
	reading_examples = json.load(f)

