from sentence_transformers import SentenceTransformer, util
import numpy as np
import json
import torch

def calculate_similarity(input_text, bug_reports):
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

    input_embedding = model.encode(input_text)

    similarity_results = []
    
    for bug_report in bug_reports:
        issue_embedding_json = bug_report.embedding
        issue_embedding_list = json.loads(issue_embedding_json)
        issue_embedding_array = np.array(issue_embedding_list)

        # Calculate cosine similarity between input_embedding and issue_embedding_array
        issue_embedding_tensor = torch.from_numpy(issue_embedding_array).float()
        similarity_score = util.pytorch_cos_sim(input_embedding, issue_embedding_tensor.unsqueeze(0))[0][0]
        

        result = {
            'issueId': bug_report.issueId,
            'issueTitle': bug_report.issueTitle,
            'issueBody': bug_report.issueBody,
            'issueURL': bug_report.issueURL,
            'similarity': similarity_score
        }
        similarity_results.append(result)

    
    sorted_results = sorted(similarity_results, key=lambda x: x['similarity'], reverse=True)

    return sorted_results



def calculate_embeddings(input):
    try:
        model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
        input_embedding = model.encode(input)
        return input_embedding
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None 