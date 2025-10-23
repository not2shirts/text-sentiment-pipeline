from fastapi import FastAPI
import joblib
from pydantic import BaseModel


app = FastAPI()


class TextInput(BaseModel):
    text: str


class PredictionModelOutput(BaseModel):
    text: str
    sentiment: str
    score: float
    confidence: str


try:
    model = joblib.load("./models/logistic_regression_model.pkl")
    vectorizer = joblib.load("./models/tfidf_vectorizer.pkl")
except Exception as err:
    print("Error loading models : ", err)


@app.post("/sentiment")
async def predict_sentiment(text: TextInput):
    input_text = text.text

    text_vec = vectorizer.transform([input_text])

    prediction = model.predict(text_vec)
    prediction_prob = model.predict_proba(text_vec)

    if prediction[0] == 1:
        sentiment = "positive"
    else:
        sentiment = "negative"

    confidence = "high"
    score = max(prediction_prob[0])
    if 0.5 < score <= 0.65:
        confidence = "low"
    elif 0.65 < score < 0.75:
        confidence = "medium"

    return {
        "text": input_text,
        "sentiment": sentiment,
        "score": score,
        "confidence": confidence,
    }
