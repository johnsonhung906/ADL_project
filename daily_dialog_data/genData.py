import json
import argparse

import spacy
from tqdm import tqdm
from collections import defaultdict



def save_data(dialog, index, file, mode):
    if mode == 1:
        data = {}
        data['query'] = dialog[:index]
        data['answer'] = dialog[index]
        line = json.dumps(data) + '\n'
        file.write(line)
    elif mode == 2:
        data = {}
        data['query'] = dialog[:index-1]
        data['answer'] = dialog[index-1]
        line = json.dumps(data) + '\n'
        file.write(line)
    elif mode == 3:
        for i in range(1, index):
            data = {}
            f_idx = 0 if i-4 < 0 else i-4
            data['query'] = dialog[f_idx: i]
            if len(data['query']) < 2:
                continue
            data['answer'] = dialog[i]
            line = json.dumps(data) + '\n'
            assert(len(data['query']) <= 4 and len(data['query']) > 0)
            file.write(line)
    elif mode == 4:
        f_idx = 0 if index-4 < 0 else index-4
        for i in range(f_idx, index):
            data = {}
            data['query'] = dialog[i: index]
            data['answer'] = dialog[index]
            line = json.dumps(data) + '\n'
            assert(len(data['query']) <= 4 and len(data['query']) > 0)
            file.write(line)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--file_split",
        default="train",
        type=str
    )
    args = parser.parse_args()

    return args

def main(args):
    with open("../scripts/final_project_scripts/keywords.json") as f:
        keywords = json.load(f)

    nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
    # lemmatize words in keywords
    for key, val in keywords.items():
        # separate words by its length (one, others)
        one_lemma = []
        multi_lemma = []
        for word in val:
            split = [token.lemma_ for token in nlp(word)]
            if len(split) >= 2:
                multi_lemma.append(" ".join(split))
            else:
                one_lemma.append(split[0])
            keywords[key] = [one_lemma, multi_lemma]
    # print(keywords)
    with open(f"{args.file_split}_dialog.jsonl", "r") as f:
        dialog = [json.loads(line) for line in f]

    statistics = []
    # f1 = open(f"{args.file_split}_1.jsonl", "w+")
    # f2 = open(f"{args.file_split}_2.jsonl", "w+")
    f3 = open(f"{args.file_split}_3.jsonl", "w")
    # f4 = open(f"{args.file_split}_4.jsonl", "w+")
    
    for d in tqdm(dialog):
        # start with the second utterance from the simulator
        for index in range(0, len(d["dialog"]), 2):
            lemma_utterance = [token.lemma_ for token in nlp(d["dialog"][index])]
            service_hits = defaultdict(int)
            for key, (one, multi) in keywords.items():
                intersection = set(one) & set(lemma_utterance)
                # check whether the word, the length is bigger than 2, is in the utterance
                for m in multi:
                    unsplit_utterance = " ".join(lemma_utterance)
                    if m in unsplit_utterance:
                        intersection.add(m)
                service_hits[key] += len(intersection)
                statistics += list(intersection)
                
            # Is there a keyword in this utterance
            isService = sum(service_hits.values()) != 0
            if isService:
                # save_data(d["dialog"], index, f1, 1)
                # save_data(d["dialog"], index, f2, 2)
                save_data(d["dialog"], index, f3, 3)
                # save_data(d["dialog"], index, f4, 4)
                break

args = parse_args()
main(args)