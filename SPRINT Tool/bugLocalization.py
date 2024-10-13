import os
import torch
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

        # Load the Peft/Lora model
        model = PeftModel.from_pretrained(model, peft_model_id)

        # Reload tokenizer to save it
        tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path, trust_remote_code=True)
        tokenizer.pad_token = tokenizer.eos_token
        tokenizer.padding_side = "right"

        # Run text generation pipeline with our next model
        prompt = (
            f"I have the following issue information for repository {repo_full_name}: {issue_data}. "
            f"The path list for all the code files are given below: {code_files_list}. "
            "Now based on the issue information and the file paths, find me the potential buggy code files. "
            "In your response output, only give the paths for the potential buggy code files as a list. "
            "Don't give anything else in output."
        )

        pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=200)
        result = pipe(f"<s>[INST] {prompt} [/INST]")
        print(result[0]['generated_text'])

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


# sudo apt remove python3-pip
# sudo apt install python3-pip


