import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Paths where model and vectorizer will be saved
MODEL_PATH = "../models/event_classifier.pkl"
VECTORIZER_PATH = "../models/tfidf_vectorizer.pkl"


def train_classifier(dataset_path):
    """
    Train TF-IDF + Logistic Regression classifier
    """

    # Load dataset
    data = pd.read_csv(dataset_path)

    # Separate input text and labels
    sentences = data["sentence"]
    labels = data["label"]

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()

    # Convert sentences to TF-IDF vectors
    X = vectorizer.fit_transform(sentences)

    # Create classifier
    model = LogisticRegression()

    # Train classifier
    model.fit(X, labels)

    # Save trained model
    joblib.dump(model, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("Model trained and saved.")


def load_model():
    """
    Load trained classifier and vectorizer
    """

    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)

    return model, vectorizer


def is_event(text):
    """
    Predict whether text represents a life event
    """

    model, vectorizer = load_model()

    # Convert text into TF-IDF vector
    X = vectorizer.transform([text])

    # Predict label
    prediction = model.predict(X)

    # Return True if event
    return prediction[0] == 1


if __name__ == "__main__":

    # Train classifier
    train_classifier("../data/event_training.csv")

    # Test predictions
    test_sentences = [
        "joined Tata Group in 1991",
        "joined the meeting yesterday",
        "became chairman in 2012",
        "became tired after work"
    ]

    for s in test_sentences:
        print(s, "→", is_event(s))