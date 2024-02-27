from django.apps import AppConfig
import pandas as pd
from django.conf import settings
import pickle
from scipy.sparse import load_npz, sparray
from sklearn.feature_extraction.text import TfidfVectorizer




class KishAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kish_app'
    data_dir = settings.BASE_DIR / 'data'


    df_songs_without_duplicates: pd.DataFrame = None
    vectorizer: TfidfVectorizer = None
    corpus: sparray = None



    def ready(self):
        self.load_df_songs_without_duplicates()
        self.load_vectorizer()
        self.load_corpus()

    def load_df_songs_without_duplicates(self):
        self.df_songs_without_duplicates = \
            pd.read_csv(
                self.data_dir / 'kish_songs_without_duplcates.csv'
            )

    def load_vectorizer(self):
        with open(self.data_dir/'vectorizer.pk', 'rb') as model_file:
            self.vectorizer = pickle.load(model_file)

    def load_corpus(self):
        self.corpus = load_npz(
            self.data_dir / 'corpus.npz'
        )


