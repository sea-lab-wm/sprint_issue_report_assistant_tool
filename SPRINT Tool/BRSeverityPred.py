import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel


def SeverityPrediction(input):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")

    # Fine-tuned model path here
    model = AutoModelForSequenceClassification.from_pretrained("./modelPrioritySeverityRTA")

    tokenized_inputs = tokenizer(input, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")

    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}
    model.to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)
        prediction_label = torch.argmax(probabilities, dim=1).cpu().numpy()
        print("The label for BR Severity:")
        print(prediction_label)

        return GetSeverityPriorityClass(prediction_label)





def GetSeverityPriorityClass(prediction_label):
    if(prediction_label == 0):
        return "Blocker"
    elif(prediction_label == 1):
        return "Major"
    elif(prediction_label == 2):
        return "Minor"
    if(prediction_label == 3):
        return "Trivial"
    if(prediction_label == 4):
        return "Critical"