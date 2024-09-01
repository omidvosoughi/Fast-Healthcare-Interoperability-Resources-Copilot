import json
from typing import Any, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from completion_phi import create_chat_completion
from frontend.src.assets.prompts import *
from get_snomed import *

app = FastAPI()

# Set your OpenAI API key here

# CORS middleware setup to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextInput(BaseModel):
    text: str

# Request model for mapping entities
class TextInput(BaseModel):
    text: str

# Request model for validating entities
class ValidateEntitiesInput(BaseModel):
    entities: str


def from_prompt(prompts, term):
    ext_prompt = [
            {"role": "system", "content": ""},
            {"role": "user", "content": ""}
    ]
    ext_prompt[-2]['content'] = prompts
    
    ext_prompt[-2]['content'] += " Respond to the user query with a json containing two keys:   -'text_01':Provide a brief summary of your task.  -'text_02':Include the extracted entities with the relevant entity types as keys and the extracted entities as values."
    
    ext_prompt[-1]['content'] = term
    # print("prompt##", ext_prompt)
    return ext_prompt

@app.get("/api/prompts/extract")
def get_extract_prompts():
    return JSONResponse(content=extract_prompts_test)

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get('message')
    # print(data.get('prom'))

    user_prompt = data.get('prom')
    # print(json.loads(user_prompt))

    
    json_text = create_chat_completion(from_prompt(user_prompt, user_message))
    
    
    try:
        # Find the position of the first '{' which indicates the start of the JSON object
        json_start_index = json_text.find('{')
        # Find the position of the last closing '}'
        json_end_index = json_text.rfind('}')

        # Extract the JSON part of the string
        json_part = json_text[json_start_index:json_end_index + 1].strip()
        
        reply_json = json.loads(json_part)
        
        text = reply_json.get('text_01')
        type = reply_json.get('text_02')

        return JSONResponse(content={'reply': text, 'general': type})
    except:
        print("There is no text for text_01 and text_02")
        return JSONResponse(content={'reply': 'error1', 'general': 'error2'})
    

@app.post("/map-entities/")
async def map_entities_to_snomed(input_data: TextInput) -> Dict[str, Any]:
    text = input_data.text

    json_text = json.loads(text)

    map_prompt = "Given following clinical entity, map it to SNOMED CT, then make it available to put in FHIR format. Please return just the display name (coming from SNOMED CT) of corresponding clinical entity as follows: <given_clinical_entity>:<display_name_from_SNOMED CT>. Please ignore the corresponding SNOMED CT codes."

    response_dict = {}

    # Iterate over each key-value pair in the dictionary
    for key, value in json_text.items():
        map_entity = ''
        map_json_text = ''
        if isinstance(value, list):  # Check if the value is a list
            if len(value) >= 1:
                print(f"{key}: 2")
                for item in value:
                    map_entity = item
                    map_json_text = create_chat_completion(from_prompt(map_prompt, map_entity))
                    # print('#mapped response:', map_json_text)
                    # Find the position of the first '{' which indicates the start of the JSON object
                    json_start_index = map_json_text.find('{')
                    # Find the position of the last closing '}'
                    json_end_index = map_json_text.rfind('}')

                    # Extract the JSON part of the string
                    map_json_part = map_json_text[json_start_index:json_end_index + 1].strip()
                    
                    map_reply_json = json.loads(map_json_part)
                    
                    summary = map_reply_json.get('text_01')
                    response_json = map_reply_json.get('text_02')
                    for x, y in response_json.items():
                        response_dict[x] = y

            else:
                print(f"{key}: 0")
        else:
            map_entity = value
            map_json_text = create_chat_completion(from_prompt(map_prompt, map_entity))
            
            # Find the position of the first '{' which indicates the start of the JSON object
            json_start_index = map_json_text.find('{')
            # Find the position of the last closing '}'
            json_end_index = map_json_text.rfind('}')

            # Extract the JSON part of the string
            map_json_part = map_json_text[json_start_index:json_end_index + 1].strip()
            
            map_reply_json = json.loads(map_json_part)
            
            summary = map_reply_json.get('text_01')
            response_json = map_reply_json.get('text_02')
            for x, y in response_json.items():
                        response_dict[x] = y


    # Dummy logic for mapping entities to SNOMED CT
    # Replace this with actual logic for your use case
    if not text:
        raise HTTPException(status_code=400, detail="No text provided")

    response_output = json.dumps(response_dict)
    # response_dict_json = json.dumps(response_dict)
    loaded_response_dict_json = json.loads(response_output)
    
    return {"message": "Entities successfully mapped to SNOMED CT.", "mapped_entities": loaded_response_dict_json}


@app.post("/validate-entities/")
async def validate_entities_with_snomed(input_data: ValidateEntitiesInput) -> Dict[str, Any]:
    entities = input_data.entities
    # print(entities)
    json_entities = json.loads(entities)

    extracted_snomed_dict = {}
    for key, value in json_entities.items():
        # print(value)
        extracted_snomed_dict[key] = get_snomed_term(value)

    # print(extracted_snomed_dict)

    similarity_dict = {}

    for key, value in extracted_snomed_dict.items():
        if value == 'No matching terms found.':
            similarity_dict[key] = 'No data.'
        else:
            similarity_list = {}
            for term,item in value.items():
                similarity_score = compute_similarity(key, item)
                similarity_list[item] = similarity_score
            similarity_dict[key] = similarity_list

    # print(similarity_dict)
    response_output = json.dumps(similarity_dict)

    loaded_response_dict_json = json.loads(response_output)

    return {"message": "Entities successfully validated with SNOMED CT.", "validation_results": loaded_response_dict_json}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
        
    

    
    


