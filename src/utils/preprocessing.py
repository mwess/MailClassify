"""
This module contains a variety of utility functions that can be used to pre process text before an analysis.
Each of the preprocessing functions takes as an input a string to be transformed and outputs
the transformed string.
"""
import re


def replace_punctuations(text: str):
    return re.sub('[?!;:]+', '.', text)


def remove_non_ascii(text):
    regex = '[^\x00-\x7F]+'
    return re.sub(regex, ' ', text)


def remove_braces(text):
    regex = r'[\(\)]+'
    return re.sub(regex, ' ', text)


def remove_trailing_arithmetic_symbols(text):
    """
    Removes trailing arithmetic symbols from tokens. Trailing meaning that they start or end the token.
    """
    regex = r'\s+[\+\*-/]+|[\+\*-/]+\s+'
    return re.sub(regex, ' ', text)


def remove_some_nonalphanums(text):
    """
    Replace some nonalphanumerical characters by spaces.
    """
    regex = r'[^\d\w.,!?:;\s]+'
    return re.sub(regex, ' ', text)


def remove_arithmetic_symbols(text):
    """
    Replace arithmethic symbols that are in no connection to other types of characters by spaces.
    """
    regex = r'\s+[\+\*-/]+\s+'
    return re.sub(regex, ' ', text)


def remove_inner_symbols(text):
    """
    Remove symbols that are in the middle of tokens.
    """
    regex = r'[-/]+'
    return re.sub(regex, ' ', text)


def reduce_http(text):
    url_regex = r'http[s]?:\S+|www.\S+'
    return re.sub(url_regex, 'http', text)


def reduce_punctuation(text):
    regex = r'[\.,:;!\?]+'
    return re.sub(regex, ' ', text)


def lowercase_chars(text: str):
    return text.lower()


def replace_trailing_dashes(text):
    regex = r'(\S+)(\-)(\s+)|(\s+)(\-)(\S+)'
    return re.sub(regex, r'\1 \3', text)


def transform_umlaute(text):
    text = text.replace('ä', 'ae').\
                replace('ö', 'oe').\
                replace('ü', 'ue').\
                replace('ß', 'ss')
    return text


def escapes_dots(text):
    return text.replace('.', '\\.')


def reduce_whitespaces(text):
    regex = r'\s+'
    return re.sub(regex, ' ', text)


main_body_delimiters = [
    'beste gruesse',
    'mit besten gruessen',
    'mit freundlichen gruessen',
    'viele gruesse',
    'liebe gruesse',
    'freundliche gruesse',
    'mfg',
    'schoene gruesse',
    # English
    'best regards',
    'kind regards',
    'regards',
    'we look forward to hearing from you',
    'sincerly',
    'sincerely',
]


def contains_body_delim(text):
    return any([x in text for x in main_body_delimiters])


def filter_main_body(text):
    lines = text.split('\n')
    ind = 0
    while not len(lines) == ind and not contains_body_delim(lines[ind]):
        ind += 1
    if ind > 0:
        ind -= 1
    return '\n'.join(lines[:ind])


def remove_pentasys_header_for_location(text):
    header = 'PENTASYS AG, mit Sitz in München, Geschäftsstellen in Frankfurt am Main, Düsseldorf, Nürnberg, Hamburg und Stuttgart, ist ein Tochterunternehmen der französischen AUSY Group mit 4.000 Mitarbeitern in 11 Ländern.'
    return text.replace(header, ' ')


generic_filter = [
    remove_pentasys_header_for_location,
    reduce_http,
    replace_punctuations,
    transform_umlaute,
    remove_non_ascii,
    lowercase_chars,
    reduce_punctuation,
    remove_arithmetic_symbols,
    remove_braces,
    filter_main_body,
]


# Filter functions for cities.


def remove_BAD_prefix(city):
    """
    Some german city names start with Bad. Since this only Marienbach appears more than once, we remove this prefix
    for now.
    """
    return city.replace('bad ', '').strip()


def remove_AM_connector(city):
    connector = ' am '
    return remove_connector_pattern(city, connector)


def remove_IM_connector(city):
    connector = ' im '
    return remove_connector_pattern(city, connector)


def remove_AN_DER_connector(city):
    connector = ' an der '
    return remove_connector_pattern(city, connector)


def remove_IN_DER_connector(city):
    connector = ' in der '
    return remove_connector_pattern(city, connector)


def remove_IN_connector(city):
    connector = ' in '
    return remove_connector_pattern(city, connector)


def remove_OB_DER_connector(city):
    connector = ' ob der '
    return remove_connector_pattern(city, connector)


def remove_BEI_connector(city):
    connector = ' bei '
    return remove_connector_pattern(city, connector)


def remove_VOR_DER_connector(city):
    connector = ' vor der '
    return remove_connector_pattern(city, connector)


def remove_connector_pattern(text, connector, first=True):
    ind = 0 if first else -1
    if connector in text:
        text = text.split(connector)[ind]
    return text


def remove_braced_information(city):
    return re.sub(r'(?:\(.*\))', '', city)  # Remove "additional data" that is placed in braces


def strip(city):
    return city.strip()

