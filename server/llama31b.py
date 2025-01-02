import torch
import json
from transformers import pipeline


class Llama321b:
    def __init__(self):
        self.model_id = "meta-llama/Llama-3.2-1B"
        self.pipe = pipeline(
            "text-generation",
            model=self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

    def Chat(self, prompt):
        output= self.pipe(json.dumps(prompt))
        return output[0]["generated_text"]
