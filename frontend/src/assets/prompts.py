# Define prompt formats
extract_prompts = [
            {"role": "system", "content": 'You are a clinical entity extractor. Your task is to process clinical notes and extract relevant FHIR resources, including following resource types:'},
            {"role": "user", "content": ""}
    ]

# extract_prompts_test = 'You are a clinical entity extractor. Your task is to process the given clinical note and extract relevant clinical entities. Specifically, identify the following entity types:'
extract_prompts_test = 'You are a clinical entity extractor. Your task is to process the following clinical note and extract relevant clinical entities for the specified entity types:'