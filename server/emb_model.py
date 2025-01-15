"""
from sentence_transformers import SentenceTransformer


class MyEmbModel():
    def __init__(self, model_dir):
        self.model = SentenceTransformer("m3e-base")

    def to_emb(self, sentence):
        if isinstance(sentence, str):
            sentence = [sentence]
        return self.model.encode(sentence)
    
"""

import requests
import json
import numpy as np


class MyEmbModel:
    def __init__(self):
        pass

    def to_emb(self, sentence: str):
        data = {"sentence": sentence}
        response = requests.post("http://39.106.90.31:1440/api/embedding", data)
        elist = json.loads(response.text)["embedding"]
        emd = np.array(elist)
        return emd


if __name__ == "__main__":
    my_documents = MyEmbModel()
    sent_vec = my_documents.to_emb("What is a large model")
    print("vec dim:", sent_vec[0])
