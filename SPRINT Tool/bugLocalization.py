import os
import torch
import re
import ast
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    pipeline,
)
from datasets import load_dataset
from peft import PeftConfig, PeftModel
from trl import SFTTrainer

def BugLocalization(issue_data, repo_full_name, code_files_list):
    try:
        peft_model_id = './Llama-2-7b-chat-finetune'
        base_model_name = 'NousResearch/Llama-2-7b-chat-hf'
        config = PeftConfig.from_pretrained(peft_model_id) 

        use_nested_quant = False
        bnb_4bit_quant_type = "nf4"
        bnb_4bit_compute_dtype = "float16"
        use_4bit = True
        compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

        bnb_config = BitsAndBytesConfig(
            load_in_4bit=use_4bit,
            bnb_4bit_quant_type=bnb_4bit_quant_type,
            bnb_4bit_compute_dtype=compute_dtype,
            bnb_4bit_use_double_quant=use_nested_quant,
        )

        model = AutoModelForCausalLM.from_pretrained(
            config.base_model_name_or_path,
            quantization_config=bnb_config,
            torch_dtype=torch.bfloat16,
            device_map="auto",
            low_cpu_mem_usage=True,
            return_dict=True,
        )

        
        model = PeftModel.from_pretrained(model, peft_model_id)

        tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"

        prompt = (
            f"I have the following issue information for repository {repo_full_name}: "
            f"Issue Data: {issue_data}\n\n"
            f"The path list for all the code files are given below: {code_files_list}. "
            "Now based on the issue information and the file paths, find me the potential buggy code files. "
            "In your response output, only give the paths for the potential buggy code files as a list. Make sure to give the exact path as given in the input. "
            "Don't give anything else in output."
        )


        pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=2048)
        result = pipe(f"<s>[INST] {prompt} [/INST]")
        generated_text = result[0]['generated_text']
        print('------------------------')
        generated_only = generated_text.split("[/INST]")[-1].strip()
        print(generated_only)
        
        list_pattern = r'\[.*?\]'
        match = re.search(list_pattern, generated_only)

        if match:
            list_str = match.group()  
            try:
                generated_list = ast.literal_eval(list_str)
                if isinstance(generated_list, list):
                    print("Converted list:", generated_list)
                    return generated_list
                else:
                    print("The extracted part is not a list.")
                    return []
            except (ValueError, SyntaxError) as e:
                 print("Error converting the string to a list:", e)
        else:
            print("No list found in the generated output.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# sudo apt remove python3-pip
# sudo apt install python3-pip


