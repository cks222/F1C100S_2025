import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class Phi():
    def __init__(self) -> None:
        torch.random.manual_seed(0)

        model = AutoModelForCausalLM.from_pretrained(
            "microsoft/Phi-3.5-mini-instruct", 
            device_map="auto",#"cpu/cuda", 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )
        tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3.5-mini-instruct")

        messages = [
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
            {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
            {"role": "user", "content": "解一个2x+3=7的方程怎么样？pelase answer in Chinese."},
        ]

        self.Pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
        )

        self.generation_args = {
            "max_new_tokens": 500,
            "return_full_text": False,
            #"temperature": 0.0,
            "do_sample": False,
        }
    def Chat(self,messages):
        output = self.Pipe(messages, **self.generation_args)
        return output[0]["generated_text"]