import torch 
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 


# Specify a directory to save the model locally
model_dir = "./model_cache"

torch.random.manual_seed(0) 
model = AutoModelForCausalLM.from_pretrained( 
    "microsoft/Phi-3-mini-4k-instruct",  
    device_map="cuda",  
    torch_dtype="auto",  
    trust_remote_code=True,  
    cache_dir=model_dir
) 

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct", cache_dir=model_dir) 

def create_chat_completion(prompts):
    pipe = pipeline( 
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
    ) 

    generation_args = { 
        "max_new_tokens": 1000, 
        "return_full_text": False, 
        # "temperature": 0.0, 
        "do_sample": False, 
    } 

    output = pipe(prompts, **generation_args) 
    return output[0]['generated_text']
