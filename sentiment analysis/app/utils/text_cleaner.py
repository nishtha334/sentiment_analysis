import string
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.base import BaseEstimator, TransformerMixin

nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

class TextCleaner(BaseEstimator, TransformerMixin):
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
        words = text.split()
        words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        return " ".join(words)

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return [self.clean_text(text) for text in X]
