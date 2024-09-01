import requests
from transformers import AutoTokenizer, AutoModel
import torch

# Specify a directory to save the model locally
model_dir = "./model_cache"

tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1", cache_dir=model_dir)
model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1", cache_dir=model_dir)

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt")
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

def get_snomed_term(term):

    # Define the base URL for the FHIR server
    base_url = 'https://snowstorm-lite.nw.r.appspot.com/fhir'

    # Define the parameters for the request
    search_term = term  # Replace with the term you want to search for
    count = 10  # Number of results to return
    offset = 0  # Start from the first result

    # Construct the full URL with parameters
    expand_url = f"{base_url}/ValueSet/$expand"
    params = {
        'url': 'http://snomed.info/sct?fhir_vs',  # SNOMED CT ValueSet URL
        'count': count,
        'offset': offset,
        'filter': search_term
    }

    # Make the GET request to the FHIR server
    response = requests.get(expand_url, params=params)

    similarity_dict = {}

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        response_data = response.json()
        
        # Extract and print the SNOMED CT codes and their descriptions
        if 'expansion' in response_data and 'contains' in response_data['expansion']:
            for item in response_data['expansion']['contains']:
                similarity_dict[item['code']] = item['display']
            
            return similarity_dict
                # return f"Code: {item['code']}, Display: {item['display']}"
        else:
            return "No matching terms found."
    else:
        return f"Failed to retrieve data: {response.status_code}"


def compute_similarity(given_term, snomed_term):
    term1_embedding = embed_text(given_term)
    term2_embedding = embed_text(snomed_term)

    cosine_similarity = torch.nn.functional.cosine_similarity(term1_embedding, term2_embedding)
    return float(cosine_similarity)