"""
This module is concered with the extraction of location information from strings.
"""
import re

from nltk import word_tokenize

import src.utils.preprocessing as pp
from src.utils.processpipeline import ProcessPipeline
from src.utils.mails import transform_mail

# List of locations for which we accept projects.
list_of_acceptable_locations = [
    'Frankfurt',
    'Frannkfurt',  # Typo
    'Wiesbaden',
    'Darmstadt',
    'Mainz',
    'Neu Isenburg',
    'Neu-Isenburg',
    'Eschborn',
    'Bad Vilbel',
    'Bad Homburg',
    # Abbreviations
    'FFM',
    # General area descriptions
    'Rhein-Main',
    'Rhein Main',
    'Rhein',
    'Main',  # Beware english mails.
    'Homburg',
    'Vilbel',
    'Isenburg',
    'ffm',
    'rhein-main',
    'rhein main',
    'rhein',
    'rhein-main-gebiet',
    'frankfurt/main',
]


city_filters = [
    pp.lowercase_chars,
    pp.remove_braced_information,
    pp.transform_umlaute,
    pp.remove_BAD_prefix,
    pp.remove_AM_connector,
    pp.remove_IM_connector,
    pp.remove_AN_DER_connector,
    pp.remove_IN_DER_connector,
    pp.remove_IN_connector,
    pp.remove_OB_DER_connector,
    pp.remove_BEI_connector,
    pp.remove_VOR_DER_connector,
    pp.escapes_dots,
    pp.strip,
]


def add_custom_keywords(cities):
    additional_keywords = [
        'ffm',
        'rhein-main',
        'rhein main',
        'rhein',
        'rhein-main-gebiet',
        'frankfurt/main',
    ]
    return cities + additional_keywords

def remove_custom_keywords(cities):
    """
    Remove the following words from cities because their semantic meaning is too ambiguous
    :param cities:
    :return:
    """
    remove_keywords = [
        'weil',
        'waren',
        'lage',
        'senden',
        'wissen',
    ]
    return [x for x in cities if x not in remove_keywords]


def add_foreign_cities():
    return [
        'Zürich',
        'Zurich',
        'Wien',
        'Vienna',
    ]


def load_city_list(fname, preprossing=True):
    city_preprocess_filter = ProcessPipeline(city_filters)
    with open(fname) as f:
        cities = f.readlines()
        cities += add_foreign_cities()
    if preprossing:
        cities = list(map(lambda city: city_preprocess_filter.execute(city), cities))
    cities = add_custom_keywords(cities)
    cities = remove_custom_keywords(cities)
    return cities


def extract_location_names(message, city_list):
    """
    message is already preprocessed
    city list has already
    """
    tokens = word_tokenize(message, language='german')
    cities = []
    for token in tokens:
        if token in city_list:
            cities.append(token)
    return cities


class LocationExtraction:

    def __init__(self, acceptable_cities):
        self._cities = acceptable_cities
        self._location_filters = []
        self._regex_prefix = r'(?=(?:^|[\s.,!?;:]){1}?'
        self._regex_suffix = r'(?:[\s.,!?;:]|$){1}?)'
        self._location_expression = ''
        self._setup_filters()
        self._build_location_regex()

    def _setup_filters(self):
        self._location_filters = [
            pp.remove_pentasys_header_for_location,
            pp.reduce_http,
            pp.replace_punctuations,
            pp.transform_umlaute,
            pp.remove_non_ascii,
            pp.lowercase_chars,
            pp.replace_trailing_dashes,
            pp.remove_arithmetic_symbols,
            pp.remove_braces,
            pp.filter_main_body,
            pp.reduce_whitespaces,
        ]

        self._region_filters = [
            pp.remove_pentasys_header_for_location,
            pp.reduce_http,
            pp.replace_punctuations,
            pp.transform_umlaute,
            pp.remove_non_ascii,
            pp.lowercase_chars,
            pp.remove_arithmetic_symbols,
            pp.remove_braces,
            pp.filter_main_body,
            pp.reduce_whitespaces,
        ]

    def extract_cities(self, message):
        locations = re.findall(self._location_expression, message)
        return locations

    def _build_location_regex(self):
        self._location_expression = self._regex_prefix + '(' + '|'.join(self._cities) + ')' + self._regex_suffix

    def extract_locations(self, mail):
        message = transform_mail(mail, self._location_filters)
        locations = self.extract_cities(message)
        regions = self.extract_region_patterns(message)
        return list(set(locations + regions))

    def extract_region_patterns(self, message):
        region_pattern_d = r'(?=([Dd]{1}[0-9]{1,5}([^.]|$)))'
        matches = re.finditer(region_pattern_d, message)
        found_regions = [match.group(1).strip() for match in matches]
        region_pattern_plz = r'(?=(plz\s*[0-9]{1,5}([^.]|$)))'
        matches = re.finditer(region_pattern_plz, message)
        found_regions += [match.group(1).strip() for match in matches]
        return found_regions

    @classmethod
    def from_file(cls, fname):
        cities = load_city_list(fname)
        return cls(cities)

    @classmethod
    def load_from_default_file(cls):
        default_file = 'models/location/german_city_tree.txt'
        return LocationExtraction.from_file(default_file)

    @staticmethod
    def extract_all_locations(mail):
        extractor = LocationExtraction.load_from_default_file()
        return extractor.extract_locations(mail)

    @staticmethod
    def contains_acceptable_locations(locations):
        acceptable_locations = list(map(lambda x: x.lower(), list_of_acceptable_locations))
        if any(map(lambda location: location in acceptable_locations, locations)):
            return True
        else:
            return False
