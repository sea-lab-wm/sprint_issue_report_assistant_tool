import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel

def DuplicateDetection(sent1, sent2):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    tokenizer = AutoTokenizer.from_pretrained("Colorful/RTA")

    # Fine-tuned model path here
    model = AutoModelForSequenceClassification.from_pretrained("./modelDupBrRTA")

    args = (
                (sent1, sent2)
            )

    tokenized_inputs = tokenizer(sent1, sent2, padding="max_length", max_length=tokenizer.model_max_length, truncation=True, return_tensors="pt")

    inputs = {key: value.to(device) for key, value in tokenized_inputs.items()}
    model.to(device)

    with torch.no_grad():
        logits = model(**inputs).logits
        probabilities = torch.softmax(logits, dim=1)
        prediction_label = torch.argmax(probabilities, dim=1).cpu().numpy()
        print("The probability for duplicate BR is:")
        print(prediction_label)

        return prediction_label



# sent1 = "move propertysetmixin helper from comphelper into the public availbale cppuhelper"
# sent2 = "The OpenFormula draft changes B() to BINOM.DIST.RANGE()\nAdd BINOM.DIST.RANGE as an alias for B so documents of future releases can be\nread in this release. Do not write BINOM.DIST.RANGE in this release."

# DuplicateDetection(sent1, sent2)
    
    