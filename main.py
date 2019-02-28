#!/bin/bash

import sys

import pandas as pd

from src.remote.remote import RemoteClassifier
from src.location.location import LocationExtraction
from src.technology.technology import TechnologyExtraction


def classify_mail_features(mail):
    retrieved_information = dict()
    retrieved_information['remote'] = RemoteClassifier.classify_remoteness(mail)
    retrieved_information['locations'] = LocationExtraction.extract_all_locations(mail)
    retrieved_information['technologies'] = TechnologyExtraction.extract_acceptable_technologies(mail)
    return retrieved_information


def decide_mail_importance(mail_attributes):
    acceptable_location = LocationExtraction.contains_acceptable_locations(mail_attributes['locations']) or mail_attributes['remote']
    acceptable_technologies = TechnologyExtraction.contains_acceptable_technologies(mail_attributes['technologies'])
    if acceptable_technologies and acceptable_location:
        mail_attributes['interesting'] = True
    else:
        mail_attributes['interesting'] = False
    return mail_attributes


def read_file(fp):
    if fp.endswith(".json"):
        return pd.read_json(fp)
    elif fp.endswith(".csv"):
        return pd.read_csv(fp)
    else:
        exit()

def german_response(b):
    return 'Ja' if b else 'Nein'

def stringify_result(dct):
    remote = 'remote: ' + german_response(dct['remote'])
    #print('Remoteness: ', dct['remote'])
    #print('Type? ' , type(dct['remote']))
    locations = 'Ort: ' + ' '.join(dct['locations'])
    technologies = 'Technologien: ' + ' '.join(dct['technologies'])
    interesting = 'Koennte interessant sein: ' + german_response(dct['interesting'])
    return '\n'.join([locations, remote, technologies, interesting])


def write_result_to_file(fp, result_str):
    with open(fp, 'w') as f:
        f.write(result_str)

def main():
    file_name = sys.argv[1]
    if len(sys.argv) != 3:
        exit()
    mails = read_file(file_name)
    results = []
    for i in range(len(mails)):
        current_mail = mails.iloc[i]
        mail_eval = classify_mail_features(current_mail)
        mail_eval['id'] = i
        mail_eval = decide_mail_importance(mail_eval)
        results.append(mail_eval)
    for idx, result in enumerate(results):
        #stringify_result(result)
        write_result_to_file(sys.argv[2], stringify_result(result))
        #print(stringify_result(result))
        #print('Remote: ', result['remote'])


if __name__ == '__main__':
    main()
