import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH_SEVERITY = os.getenv("SEVERITY_PREDICTION_MODEL_PATH")

def SeverityPrediction(input_text):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH_SEVERITY)

    tokenized_inputs = tokenizer(
        input_text, 
        padding="max_length", 
        max_length=tokenizer.model_max_length, 
        truncation=True, 
        return_tensors="pt"
    )
    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}

    model.to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)
        prediction_label = torch.argmax(probabilities, dim=1).cpu().numpy()

        print("The label for BR Severity:")
        print(prediction_label)

        return GetSeverityPriorityClass(prediction_label[0])  

def GetSeverityPriorityClass(prediction_label):
    severity_classes = {
        0: "Blocker",
        1: "Major",
        2: "Minor",
        3: "Trivial",
        4: "Critical",
    }
    return severity_classes.get(prediction_label, "Unknown")
