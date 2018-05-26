from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class Predict(object):
    def __init__(self):
        self.estimator = joblib.load('supervised_model.pkl')
        self.vectorizer = joblib.load('supervised_vectorizer.pkl')

    def predict(self, text):
        makelist = []
        makelist.append(text)
        X = self.vectorizer.transform(makelist)
        return dict(zip(self.estimator.classes_, list(self.estimator.predict_proba(X)[0])))
