"""
Technology information extraction.
"""

import re

import src.utils.preprocessing as pp
from src.utils.processpipeline import ProcessPipeline
from src.utils.regex import build_regexpr_from_list
#from src.utils.mails import transform_mail


list_of_possible_technologies = [
    'Java',
    'java',
    'jee',
    'java ee',
    'Typescript',
    'Angular',
    'Angular2',
    'Angular 2',
    'Spring',
    'Spring-boot',
    'springboot',
#    'SQL',
]


def process_technologies(l):
    for i, v in enumerate(l):
        l[i] = v.lower()
    return l


def transform_mail(mail, custom_filters):
    pipeline = ProcessPipeline(custom_filters)
    message = mail['Betreff'] + '\n' + mail['Text']
    return pipeline.execute(message)


class TechnologyExtraction:
    """
    Class to extract technologies from mails.
    """

    def __init__(self, technologies):
        self._technologies = technologies
        self._technology_filters = []
        self._setup_filters()

    def _setup_filters(self):
        self._technology_filters = pp.generic_filter

    @staticmethod
    def contains_acceptable_technologies(technologies):
        return len(technologies) > 0

    def extract_technologies(self, mail):
        message = transform_mail(mail, self._technology_filters)
        techno_expr = build_regexpr_from_list(self._technologies)
        return list(set(re.findall(techno_expr, message)))

    @classmethod
    def load_default(cls):
        acceptable_technologies = process_technologies(list_of_possible_technologies)
        return cls(acceptable_technologies)

    @staticmethod
    def extract_acceptable_technologies(mail):
        extractor = TechnologyExtraction.load_default()
        return extractor.extract_technologies(mail)
