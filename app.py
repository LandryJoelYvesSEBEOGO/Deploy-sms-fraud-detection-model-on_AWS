from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from peft import PeftModel
import uvicorn

app = FastAPI()

# Configuration des CORS.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permettre toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
base_model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased")
model = PeftModel.from_pretrained(base_model, "MrNWARMeilleur/sms_fraud_detection")

classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

class SMSRequest(BaseModel):
    message: str

@app.post("/predict")
async def predict(sms: SMSRequest):
    prediction = classifier(sms.message)
    if prediction[0]['label'] == 'LABEL_0':
        prediction = "This message is not a fraud"
    else:
        prediction = "This message is a fraud"
    return prediction

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080, reload=True)