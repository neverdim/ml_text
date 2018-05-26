import pandas as pd # библиотека для работы с массивами данных
import numpy as np # библиотека для массивов и математических выражений

# библиотека для mongodb
from pymongo import MongoClient

# классификатор "случайные деревья"
from sklearn.ensemble import RandomForestClassifier

# разбиение на выборки и перебор параметров
from sklearn.model_selection import GridSearchCV, train_test_split, StratifiedKFold

# результат на отложенной выборке
from sklearn.metrics import accuracy_score

# перевод текста в числовую матрицу (словарь, вес слов)
from sklearn.feature_extraction.text import TfidfVectorizer

# сохранение и загрузка моделей
from sklearn.externals import joblib


issues = pd.DataFrame()

client = MongoClient()

db = client.ml_database

issues = pd.DataFrame.from_records(db.ml_collection.find())

issues_train, issues_test, labels_train, labels_test = (
    train_test_split(issues.content, issues.category, test_size=0.3, stratify=issues.category)
                                                        )

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(issues_train)

classifier = RandomForestClassifier()


# Закоментил параметры, перебор по которым требует больше мощностей
param_grid = {
    'n_estimators': np.arange(20, 101, 10),
    'min_samples_split': np.arange(2, 11, 1),
    # 'max_depth': np.arange(1,11,1),
    # 'max_features': np.arange(4,19, 2)
            }

estimator = GridSearchCV(classifier, param_grid=param_grid, cv=StratifiedKFold(n_splits=5).split(issues_train, labels_train))

estimator.fit(X, labels_train)

accuracy = accuracy_score(estimator.best_estimator_.predict(vectorizer.transform(issues_test)
                                                ), labels_test)
db.ml_accuracy.drop()
db.ml_accuracy.insert_one({'item': 'accuracy', 'value': accuracy})

joblib.dump(estimator.best_estimator_, 'supervised_model.pkl') # обученная модель
joblib.dump(vectorizer, 'supervised_vectorizer.pkl') # словарь с параметрами
