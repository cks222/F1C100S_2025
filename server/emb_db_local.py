import os
import json
import threading
from typing import List
from datetime import datetime
import hashlib
import numpy as np


class MyMilvusData:
    def __init__(self, category: str, vector: List[float], question: str, answer: str):
        self.id = hashlib.sha256((category + question).encode("utf-8")).hexdigest()
        self.vector = vector
        self.question = question
        self.answer = answer
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class MyEmbDbClient:
    def __init__(self, DbDir="C:\\db\\EmbDb"):
        self.output_fields = ["question", "answer"]
        self.fields_name = [
            "id",
            "vector",
            "question",
            "answer",
            "timestamp",
        ]

        self.knowledgefilelocks = {}
        self.Dir = DbDir
        if not os.path.exists(DbDir):
            os.mkdir(DbDir)

    def build_data(
        self, category: str, vector: List[float], question: str, answer: str
    ):
        return MyMilvusData(
            category=category,
            vector=vector,
            question=question,
            answer=answer,
        )

    def insert_data(self, knowledgeid, data: List[MyMilvusData]) -> None:
        if len(data) == 0:
            return
        ist_data = [
            {field: getattr(d, field) for field in self.fields_name} for d in data
        ]
        olddata = []
        olddata.extend(ist_data)
        self._save(knowledgeid, olddata)

    def search_similar(self, vector: List[float], knowledgeid, top_k: int = 3) -> List:
        alldata = self._read(knowledgeid)
        if len(alldata) == 0:
            return []
        return self.find_top_n_similar(alldata, vector, top_k)

    def _checklockexist(self, knowledgeid):
        if knowledgeid not in self.knowledgefilelocks.keys():
            self.knowledgefilelocks[knowledgeid] = threading.Lock()

    def _read(self, knowledgeid):
        self._checklockexist(knowledgeid)
        with self.knowledgefilelocks[knowledgeid]:
            path = os.path.join(self.Dir, knowledgeid + ".emb.json")
            if os.path.exists(path):
                with open(path, "r") as file:
                    data = json.load(file)
            else:
                data = []
        return data

    def _save(self, knowledgeid, data):
        self._checklockexist(knowledgeid)
        with self.knowledgefilelocks[knowledgeid]:
            with open(os.path.join(self.Dir, knowledgeid + ".emb.json"), "w") as file:
                json.dump(data, file)

    def cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def find_top_n_similar(self, data, search_vector, n=3):
        similarities = []

        for item in data:
            similarity = self.cosine_similarity(
                np.array(item["vector"]), np.array(search_vector)
            )
            similarities.append(
                (similarity, {"question": item["question"], "answer": item["answer"]})
            )
        similarities.sort(key=lambda x: x[0], reverse=True)

        # 取前 n 个最相似的对象
        top_n = similarities[:n]

        # 返回 name 和 id
        return [
            {"question": item[1]["question"], "answer": item[1]["answer"]}
            for item in top_n
        ]
