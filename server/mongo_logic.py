from pymongo import MongoClient
import uuid
import os


class MongoLogic:
    def __init__(self):

        isProd = os.getenv("isProd") == "true"
        host = "mongodb" if isProd else "localhost"
        self.client = MongoClient("mongodb://admin:admin@" + host + ":27017")
        db_name = "Chat"
        self.db = self.client[db_name]
        self.Usercollection = self.get_col("User")
        self.Knowledgecollection = self.get_col("Knowledge")
        self.QAcollection = self.get_col("QA")
        self.ChatHistorycollection = self.get_col("ChatHistory")
        self.ChatSessioncollection = self.get_col("Session")

    def get_col(self, collection_name: str):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
        return self.db.get_collection(collection_name)

    def getGuid(self):
        return str(uuid.uuid4())

    def add_user(self, username: str, encrypted_str: str):
        data = {
            "data": {
                "id": self.getGuid(),
                "username": username,
                "encrypted_str": encrypted_str,
            }
        }
        self.Usercollection.insert_one(data)

    def get_user(self, username: str, encrypted_str: str):
        query = {
            "$and": [{"data.username": username}, {"data.encrypted_str": encrypted_str}]
        }
        data = self.Usercollection.find_one(query)
        return "" if data is None else data["data"]

    def has_user(self, username: str) -> bool:
        query = {"data.username": username}
        data = self.Usercollection.find(query)
        return len(data) > 0

    def add_knowledge(self, username: str, knowledgename: str, ispublic: bool):
        data = {
            "data": {
                "id": self.getGuid(),
                "username": username,
                "knowledgename": knowledgename,
                "ispublic": ispublic,
                "currentversion": "",
            }
        }
        self.Knowledgecollection.insert_one(data)

    def get_knowledges(self, username: str, containspublic: bool):
        if containspublic:
            query = {"$or": [{"data.username": username}, {"data.ispublic": True}]}
        else:
            query = {"data.username": username}
        data = self.Knowledgecollection.find(query)
        return [d["data"] for d in data]

    def get_knowledge_byid(self, knowledgeid: str):
        query = {"data.id": knowledgeid}
        data = self.Knowledgecollection.find_one(query)
        return data["data"]

    def edit_knowledge(self, knowledgeid: str, knowledge: dict):
        query = {"data.id": knowledgeid}
        newvalues = {"$set": {"data": knowledge}}
        self.Knowledgecollection.update_one(query, newvalues)

    def add_qas(self, knowledgeid: str, qas: list[dict]):
        data = []
        for qa in qas:
            data.append(
                {
                    "data": {
                        "id": self.getGuid(),
                        "knowledgeid": knowledgeid,
                        "q": qa["q"],
                        "a": qa["a"],
                        "e": qa["e"],
                        "isdisabled": False,
                    }
                }
            )
        self.QAcollection.insert_many(data)

    def get_qas(self, knowledgeid: str):
        query = {
            "$and": [{"data.knowledgeid": knowledgeid}, {"data.isdisabled": False}]
        }
        data = self.QAcollection.find(query)
        return [d["data"] for d in data]

    def remove_qa(self, knowledgeid: str, qa_ids: list[str]):
        query = {
            "$and": [{"data.knowledgeid": knowledgeid}, {"data.id": {"$in": qa_ids}}]
        }
        newvalues = {"$set": {"data.isdisabled": True}}
        self.QAcollection.update_many(query, newvalues)

    def edit_qa(self, knowledgeid: str, qas: list[dict]):
        for qa in qas:
            query = {"$and": [{"data.knowledgeid": knowledgeid}, {"data.id": qa["id"]}]}
            newvalues = {
                "$set": {"data.q": qa["q"], "data.a": qa["a"], "data.e": qa["e"]}
            }
            self.QAcollection.update_one(query, newvalues)

    def add_new_session(self, username: str, knowledgeid: str):
        sessionid = self.getGuid()
        data = {
            "data": {
                "sessionid": sessionid,
                "username": username,
                "knowledgeid": knowledgeid,
                "isdisabled": False,
            }
        }
        self.ChatSessioncollection.insert_one(data)
        return sessionid

    def add_new_history(
        self, sessionid: str, q: str, qtime: str, a: str, atime: str, pormpt: str
    ):
        data = {
            "data": {
                "sessionid": sessionid,
                "q": q,
                "qtime": qtime,
                "a": a,
                "atime": atime,
                "pormpt": pormpt,
            }
        }
        self.ChatHistorycollection.insert_one(data)
        return sessionid

    def get_chat_history(self, sessionid: str):
        query = {"data.sessionid": sessionid}
        data = self.ChatHistorycollection.find(query)
        return [d["data"] for d in data]

    def get_sessions(self, username: str):
        query = {"$and": [{"data.username": username}, {"data.isdisabled": False}]}
        data = self.ChatSessioncollection.find(query)
        return [d["data"] for d in data]

    def get_sessions_byid(self, sessionid: str):
        query = {"data.sessionid": sessionid}
        data = self.ChatSessioncollection.find_one(query)
        return data["data"]
