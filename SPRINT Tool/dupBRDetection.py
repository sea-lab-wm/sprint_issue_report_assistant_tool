import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from dotenv import load_dotenv

load_dotenv()

MODEL_PATH_DUPLICATE_BR = os.getenv("DUPLICATE_BR_MODEL_PATH")

def DuplicateDetection(sent1, sent2, issue_id):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH_DUPLICATE_BR)

    tokenized_inputs = tokenizer(
        sent1, 
        sent2, 
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

        print("The probability for duplicate BR is:")
        print(probabilities)
        print("Predicted label:", prediction_label)

        return prediction_label





    




    