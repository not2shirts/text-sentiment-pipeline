import joblib

model = joblib.load('../model_training/models/logistic_regression_model.pkl')
vectorizer = joblib.load('../model_training/models/tfidf_vectorizer.pkl')

text = "this was a pretty good movie the plot was great but the acting was amazing"

    # vectorize the input text
text_vec = vectorizer.transform([text])

    # make prediction
prediction = model.predict(text_vec)
prediction_proba = model.predict_proba(text_vec)
print("prediction:", prediction)
print("prediction probability:", prediction_proba)
sentiment = "positive" if prediction[0] == 1 else "negative"
score = max(prediction_proba[0])
print(f"Sentiment: {sentiment}, Score: {score:.4f}")
