import torch
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.metrics import accuracy_score, precision_score, recall_score

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")
model_path = "/kaggle/input/dupbrfinetunedmodel/model"
model = AutoModelForSequenceClassification.from_pretrained(model_path)

model.to(device) 

csv_path = '/kaggle/input/dup-br-universalencoder/dup_br_detection_data/dup_test.csv'  # add your model path here
df = pd.read_csv(csv_path)

# Assuming 'label' column has values 'yes' and 'no', convert them to binary labels [0, 1]
df['label'] = df['label'].apply(lambda x: 1 if x == 'yes' else 0)

df.head()

true_labels = []
predicted_labels = []

for index, row in df.iterrows():
    bug1 = row['bug1']
    bug2 = row['bug2']
    true_label = row['label']
    
    # Tokenize input sentences
    args = (bug1, bug2)
    tokenized_inputs = tokenizer(*args, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")
    
    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}
    
    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)

        prediction_label = torch.argmax(probabilities, dim=1).cpu().item()
        
        true_labels.append(true_label)
        predicted_labels.append(prediction_label)

# Calculate evaluation metrics
accuracy = accuracy_score(true_labels, predicted_labels) * 100
precision = precision_score(true_labels, predicted_labels) * 100
recall = recall_score(true_labels, predicted_labels) * 100

print(f"Accuracy: {accuracy:.4f}%")
print(f"Precision: {precision:.4f}%")
print(f"Recall: {recall:.4f}%")

