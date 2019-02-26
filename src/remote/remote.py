"""
Remote module. Contains models and parameters necessary to determine if a project is remote or not.
"""

import pickle

from nltk import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import RidgeClassifier

import src.utils.preprocessing as pp
from src.utils.processpipeline import ProcessPipeline

remote_filters = [
    pp.reduce_http,
    pp.replace_punctuations,
    pp.transform_umlaute,
    pp.remove_non_ascii,
    pp.lowercase_chars,
    pp.reduce_punctuation,
    pp.remove_arithmetic_symbols,
    pp.remove_braces,
    pp.filter_main_body,
]

def transform_mail(mail):
    # Join Betreff and Text
    message = mail['Betreff'] + '\n' + mail['Text']
    pipeline = ProcessPipeline(remote_filters)
    return pipeline.execute(message)



def _has_remoteness_mention(text):
    keyword = 'remote'
    return keyword in text


def locate_partial_keyword(keyword, l):
    """
    keyword: substring to be matched.
    l: list of tokens.
    returns: list of inidices indicating which token matched the keyword at least partially.
    """
    occurences = []
    for i, v in enumerate(l):
        if keyword in v:
            occurences.append(i)
    return occurences


def filter_remote_neighborhood(text):
    """
    Slice out the neighborhood of the remoteness mention.
    """
    keyword = 'remote'
    neighborhoods = []
    neighborhood_size = 8
    if keyword in text:
        tokens = word_tokenize(text)
        idxs = locate_partial_keyword(keyword, tokens)
        for idx in idxs:
            l_idx = max(idx - neighborhood_size, 0)
            u_idx = min(idx + neighborhood_size, len(tokens))
            tmp_neighborhood = tokens[l_idx: u_idx]
            neighborhoods.append(' '.join(tmp_neighborhood))
    return neighborhoods


def _choose_result(pred_list):
    return any(pred_list)
    #return not all(pred_list)


NEIGHBORHOOD_SIZE = 8
LOWER_NGRAM_RANGE = 1
UPPER_NGRAM_RANGE = 3
MIN_DF = 3
MAX_DF = 0.9


class RemoteClassifier:
    """
    Remote classifier that is used to classify possible remotes in a project.
    """

    feature_model_path = 'models/remote/feature_model'
    classification_model_path = 'models/remote/classifier_model'

    def __init__(self, feature_path, model_path):
        self._feature_path = feature_path
        self._model_path = model_path
        self._model = None
        self._features = None
        self.load_model()
        self.load_features()

    def load_model(self):
        with open(self._model_path, 'rb') as f:
            self._model = pickle.load(f)

    def load_features(self):
        with open(self._feature_path, 'rb') as f:
            self._features = pickle.load(f)

    def process_text(self, mail):
        """
        Classifies a mail for remoteness.
        returns 1 if a the mail offers the possibility of full remoteness else 0.
        """
        message = transform_mail(mail)
        if not _has_remoteness_mention(message):
            return False
        neighborhoods = filter_remote_neighborhood(message)
        feature_vectors = map(lambda substring: self.to_feature_vec([substring]), neighborhoods)
        classification_results = map(lambda features: self._model.predict(features), feature_vectors)
        return _choose_result(classification_results)

    def to_feature_vec(self, text):
        features = self._features.transform(text)
        return features

    @staticmethod
    def classify_remoteness(mail):
        rc = RemoteClassifier(RemoteClassifier.feature_model_path,
                              RemoteClassifier.classification_model_path)
        return rc.process_text(mail)
