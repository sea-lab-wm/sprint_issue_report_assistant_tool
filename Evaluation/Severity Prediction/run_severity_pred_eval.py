import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")
model_path = "/kaggle/input/modelseveritypred/modelPrioritySeverity"
model = AutoModelForSequenceClassification.from_pretrained(model_path)

model.to(device) 

csv_path = '/kaggle/input/severityprediction/severity_test.csv'
df = pd.read_csv(csv_path)

label_map = {
    "blocker": 0,
    "critical": 1,
    "major": 2,
    "minor": 3,
    "trivial": 4
}


df['label'] = df['label'].map(label_map)
df.head()

true_labels = []
predicted_labels = []

for index, row in df.iterrows():
    sentence = row['sentence1']
    true_label = row['label']
    
    # Tokenize input sentence
    tokenized_inputs = tokenizer(sentence, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")
    
    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}
    
    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)

        prediction_label = torch.argmax(probabilities, dim=1).cpu().item()
        
        true_labels.append(true_label)
        predicted_labels.append(prediction_label)

# Calculate evaluation metrics
accuracy = accuracy_score(true_labels, predicted_labels) * 100
precision = precision_score(true_labels, predicted_labels, average='weighted') * 100
recall = recall_score(true_labels, predicted_labels, average='weighted') * 100

print(f"Accuracy: {accuracy:.4f}%")
print(f"Precision: {precision:.4f}%")
print(f"Recall: {recall:.4f}%")

