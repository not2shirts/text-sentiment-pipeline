

import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd


data = joblib.load('./data/imdb_processed.pkl')




# print("Data loaded successfully.", print(data.head()))
X = data['review']
y = data['sentiment']

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

#text vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train).toarray()
X_test_vec = vectorizer.transform(X_test).toarray()


model = LogisticRegression(max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy*100:.2f}%")
joblib.dump(model, './models/logistic_regression_model.pkl')
joblib.dump(vectorizer, './models/tfidf_vectorizer.pkl')
print("Model trained and saved successfully.")
