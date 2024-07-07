import torch
from torch import nn
from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
class CustomClassifier(nn.Module):
    def __init__(self, base_model, num_labels):
        super(CustomClassifier, self).__init__()
        self.base_model = base_model
        self.dropout = nn.Dropout(p=0.1)
        self.classifier = nn.Linear(2 * base_model.config.hidden_size, num_labels)

    def forward(self, combined_embeddings):
        pooled_output = self.dropout(combined_embeddings)
        logits = self.classifier(pooled_output)
        return logits

def DuplicateDetectionComparison(sent1, sent2, model_name="Colorful/RTA", model_path="./modelDupBrRTA"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    base_model = AutoModel.from_pretrained(model_name)
    classification_model = AutoModelForSequenceClassification.from_pretrained(model_path)
    base_model.to(device)
    classification_model.to(device)

    def extract_embeddings(sent):
        tokenized_inputs = tokenizer(sent, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")
        inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}

        with torch.no_grad():
            outputs = base_model(**inputs)
            last_hidden_states = outputs.last_hidden_state  # Last hidden layer states

        return last_hidden_states.cpu()

    def combine_embeddings(embeddings1, embeddings2):
        cls_embedding1 = embeddings1[:, 0, :]  # Extract the [CLS] token embedding
        cls_embedding2 = embeddings2[:, 0, :]  # Extract the [CLS] token embedding
        combined_embeddings = torch.cat((cls_embedding1, cls_embedding2), dim=1)
        return combined_embeddings

    # Direct input prediction
    tokenized_inputs = tokenizer(sent1, sent2, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}
    with torch.no_grad():
        logits_direct = classification_model(**inputs).logits
        probabilities_direct = torch.softmax(logits_direct, dim=1)
        prediction_label_direct = torch.argmax(probabilities_direct, dim=1).cpu().numpy()

    # Extract embeddings for each sentence
    embeddings1 = extract_embeddings(sent1).to(device)
    embeddings2 = extract_embeddings(sent2).to(device)

    # Combine embeddings
    combined_embeddings = combine_embeddings(embeddings1, embeddings2).to(device)

    # Load the custom classification model
    custom_model = CustomClassifier(base_model, classification_model.config.num_labels)
    custom_model.to(device)

    # Combined embeddings prediction
    with torch.no_grad():
        logits_combined = custom_model(combined_embeddings)
        probabilities_combined = torch.softmax(logits_combined, dim=1)
        prediction_label_combined = torch.argmax(probabilities_combined, dim=1).cpu().numpy()

    print("Direct input prediction:", prediction_label_direct)
    print("Combined embeddings prediction:", prediction_label_combined)

    return prediction_label_direct, prediction_label_combined

# Example usage:
sent1 = "IN the category minor annoyances - when saving a word document (but I assume it is a general ui problem) the progress bar appears in the middle of the screen instead of in the status bar at the bottom."
sent2 = "when oo.org is started (from commandline so that only empty container window is opened), it can be seen that handle of the standard toolbar is drawn correctly and then it's covered by grey area. reproducible both with gtk and generic themes. if that toolbar is moved, handle is displayed correctly afterwards."
direct_prediction, combined_prediction = DuplicateDetectionComparison(sent1, sent2)
print("Prediction using direct input:", direct_prediction)
print("Prediction using combined embeddings:", combined_prediction)
