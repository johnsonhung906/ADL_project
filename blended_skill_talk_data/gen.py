from datasets import load_dataset
from tqdm import tqdm
import json
import csv

dataset = load_dataset("blended_skill_talk")
dataset = dataset.map(
    remove_columns=[
        "free_messages",
        "guided_messages",
        "suggestions",
        "personas",
        "additional_context",
        # "previous_utterance",
    ],
)

keywords = json.load(open("../scripts/final_project_scripts/keywords.json", "r"))
key_word_list = []
key_word_list.extend(keywords['restaurant'])
key_word_list.extend(keywords['hotel'])
key_word_list.extend(keywords['movie'])
key_word_list.extend(keywords['song'])
key_word_list.extend(keywords['transportation'])
key_word_list.extend(keywords['attraction'])

cnt = 0
jsonlFile = open("output_145.jsonl", "w")

# 145 / 4819+1009 = 2.48%
for dataset_name in ['train', 'validation']:
    for index, context in enumerate(tqdm(dataset[dataset_name])):
        for w in key_word_list:
            if w in context['previous_utterance'][0].split() and w in context['previous_utterance'][1].split():
                d = {}
                d['id'] = cnt
                d['dialog'] = ["aa", "bb"]
                d['dialog'].append(context["previous_utterance"][0])
                d['dialog'].append(context["previous_utterance"][1])
                print(json.dumps(d), file=jsonlFile)
                cnt += 1
                break

cnt = 0
jsonlFile = open("output_1613.jsonl", "w")
# 1609 / 4819+1009 = 27.6%
for dataset_name in ['train', 'validation']:
    for index, context in enumerate(tqdm(dataset[dataset_name])):
        for w in key_word_list:
            if w in context['previous_utterance'][0].split() or w in context['previous_utterance'][1].split():
                d = {}
                d['id'] = cnt
                d['dialog'] = ["aa", "bb"]
                if w in context['previous_utterance'][0].split():
                    d['dialog'].append(context["previous_utterance"][0])
                if w in context['previous_utterance'][1].split():
                    d['dialog'].append(context["previous_utterance"][1])
                print(json.dumps(d), file=jsonlFile)
                cnt += 1
                break