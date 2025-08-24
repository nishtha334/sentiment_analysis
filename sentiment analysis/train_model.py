import pandas as pd
import string
import joblib
import nltk
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from app.utils.text_cleaner import TextCleaner

# Download NLTK assets
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load data
df = pd.read_csv("reviews.txt", sep="\t", header=None, names=["review", "label"])

# --- Custom Text Preprocessing Class ---
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
        return X.apply(self.clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df["review"], df["label"], test_size=0.2, random_state=42)

# Pipeline with preprocessing + TF-IDF + RandomForest
pipeline = Pipeline([
    ('cleaner', TextCleaner()),
    ('tfidf', TfidfVectorizer(max_df=0.9, min_df=2, ngram_range=(1,2))),
    ('clf', RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42))
])

# Train model
pipeline.fit(X_train, y_train)

# Evaluate
acc = pipeline.score(X_test, y_test)
print(f"✅ Accuracy: {acc:.4f}")

# Save model
joblib.dump(pipeline, "models/sentiment_model.pkl")
print("✅ Model saved at models/sentiment_model.pkl")
