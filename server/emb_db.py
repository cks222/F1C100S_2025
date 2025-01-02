import os
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from typing import List

# from emb_model import MyEmbModel
from datetime import datetime
import hashlib


class MyMilvusData:
    def __init__(self, category: str, vector: List[float], question: str, answer: str):
        self.id = hashlib.sha256((category + question).encode("utf-8")).hexdigest()
        self.vector = vector
        self.question = question
        self.answer = answer
        self.category = category
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")


class MyMilvusClient:
    def __init__(
        self,
        host: str = "localhost",
        port: str = "19530",
        collection_name: str = "knowledge",
    ):
        isProd = os.getenv('isProd') == 'true'
        self.host =  "milvus" if isProd else host
        self.port = port
        self.collection_name = collection_name
        self.fields_name = []
        self.output_fields = ["category", "question", "answer"]
        connections.connect("default", host=self.host, port=self.port)

    def _create_collection(
        self, dim: int, idlength: int, timesteplength: int
    ) -> Collection:
        fields = [
            FieldSchema(
                name="id", is_primary=True, dtype=DataType.VARCHAR, max_length=idlength
            ),
            FieldSchema(name="category", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=dim),
            FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(name="answer", dtype=DataType.VARCHAR, max_length=5000),
            FieldSchema(
                name="timestamp", dtype=DataType.VARCHAR, max_length=timesteplength
            ),
        ]
        if len(self.fields_name) == 0:
            self.fields_name = [f.name for f in fields]
        schema = CollectionSchema(fields, self.collection_name)
        collection = Collection(self.collection_name, schema)
        index_param = {"index_type": "FLAT", "metric_type": "L2", "params": {}}
        collection.create_index("vector", index_param)
        collection.load()
        return collection

    def insert_data(self, data: List[MyMilvusData]) -> None:
        self._create_collection(
            len(data[0].vector),
            len(data[0].id),
            len(data[0].timestamp),
        )
        collection = Collection(self.collection_name)
        data = self.filter_data_existence(data)
        if len(data) == 0:
            return
        ist_data = [[getattr(d, field) for d in data] for field in self.fields_name]
        collection.insert(ist_data)
        collection.load()

    def search_similar(
        self, vector: List[float], category: str = "all", top_k: int = 3
    ) -> List:
        collection = Collection(self.collection_name)
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        expr = ""
        if category != "all":
            expr = f"category == '{category}'"
        results = collection.search(
            [vector],
            "vector",
            search_params,
            output_fields=self.output_fields,
            limit=top_k,
            expr=expr,
        )
        return [{"question":r.get("question"),"answer":r.get("answer")} for r in results[0]]

    def _delete_collection(self) -> None:
        try:
            collection = Collection(self.collection_name)
            collection.drop()
        except:
            print("can't drop")

    def get_all_data_paginated(
        self,
        category: str = "all",
        page_number: int = 1,
        page_size: int = 100,
        output_fields=[],
    ):
        if len(output_fields) == 0:
            output_fields = self.output_fields
        collection = Collection(self.collection_name)
        offset = (page_number - 1) * page_size
        expr = ""
        if category != "all":
            expr = f" and category == '{category}'"
        results = collection.query(
            expr='timestamp like"%:%"'+expr,
            offset=offset,
            limit=page_size,
            output_fields=output_fields
        )
        return results

    def filter_data_existence(self, data: List[MyMilvusData]) -> List[int]:
        page_number = 1
        newids = set([d.id for d in data])
        while True:
            results = self.get_all_data_paginated(
                page_number=page_number, output_fields=["id"]
            )
            if not results:
                break
            dbids = set([result["id"] for result in results])
            newids = newids - dbids
            if len(newids) == 0:
                return []

            page_number = page_number + 1
        new_arr = [item for item in data if item.id in newids]
        return new_arr
