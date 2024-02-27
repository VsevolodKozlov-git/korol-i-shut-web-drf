from razdel import tokenize
from nltk.corpus import stopwords
import pymorphy3

def tokenize_and_base(text):
    morph = pymorphy3.MorphAnalyzer()

    russian_stopwords = set(stopwords.words('russian'))
    additional_stopwords = {'и', 'припев', 'но', 'я', 'в', 'но', 'что', 'мой', 'свой', 'весь', 'всё', 'на',
                            'мы',
                            'c', 'a', 'вест', 'это', 'сам'}
    russian_stopwords.update(additional_stopwords)
    words = [i.text for i in tokenize(text)]
    processed_words = []
    for word in words:
        # Remove punctuation
        if not word.isalpha():
            continue
        # Remove stopwords
        if word in russian_stopwords:
            continue
        # lemmatiza
        parsed_word = morph.parse(word)[0]
        normal_form = parsed_word.normal_form
        # Check stopword in lematized
        if normal_form in russian_stopwords:
            continue
        processed_words.append(normal_form)
    return processed_words
