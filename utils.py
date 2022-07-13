import pandas as pd
import re
import string
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


def read_comments(csv_file_name, column):
    comment_texts = pd.read_csv(csv_file_name,
                                usecols=[column],
                                header=0,
                                keep_default_na=False,
                                )
    return comment_texts


def convert_to_lowercase(text):
    return text.lower()


def remove_emoticons(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001F917-\U0001F923"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_numbers(text):
    regex = r"[0-9]"
    return re.sub(regex, " ", text)


def remove_punctuations(text):
    regex = r'[' + string.punctuation + ']'
    return re.sub(regex, " ", text)


def remove_stopwords(text):
    extra_stop_words = ['told', 'one', 'two', 'three', 'say', 'says', 'said', 'also', 'according', 'year', 'years',
                        'also', 'another', 'first', 'second', 'third', 'could', 'would', 'new', 'time', 'many', 'may',
                        'even', 'well', 'still', 'got']
    stopwordset = set(stopwords.words('english')).union(set(ENGLISH_STOP_WORDS)).union(extra_stop_words)
    clean_text = " ".join([word for word in str(text).split() if word not in stopwordset])
    return clean_text


def cleanup_text(text):
    text_lc = convert_to_lowercase(text)
    clean_text = remove_numbers(text_lc)
    clean_text = remove_punctuations(clean_text)
    clean_text = remove_emoticons(clean_text)
    clean_text = remove_stopwords(clean_text)
    return clean_text
