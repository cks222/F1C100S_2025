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

    def add_user(self, account: str, encrypted_str: str):
        data = {
            "data": {
                "id": self.getGuid(),
                "username": account,
                "account": account,
                "encrypted_str": encrypted_str,
            }
        }
        self.Usercollection.insert_one(data)

    def login(self, account: str, encrypted_str: str):
        query = {
            "$and": [{"data.account": account}, {"data.encrypted_str": encrypted_str}]
        }
        data = self.Usercollection.find_one(query)
        return (
            {"id": "", "username": "", "message": "no that user"}
            if data is None
            else {"id": data["data"]["id"], "username": data["data"]["username"]}
        )

    def login_by_id(self, id: str, encrypted_str: str):
        query = {"$and": [{"data.id": id}, {"data.encrypted_str": encrypted_str}]}
        data = self.Usercollection.find_one(query)
        return (
            {"id": "", "username": "", "message": "no that user"}
            if data is None
            else {"id": data["data"]["id"], "username": data["data"]["username"]}
        )

    def get_user_by_id(self, userid: str):
        query = {"data.id": userid}
        data = self.Usercollection.find_one(query)
        return (
            {"id": "", "username": "", "message": "no that user"}
            if data is None
            else {"id": data["data"]["id"], "username": data["data"]["username"]}
        )

    def api_has_account(self, account: str) -> bool:
        query = {"data.account": account}
        data = self.Usercollection.find(query)
        return len(data) > 0

    def add_knowledge(self, userid: str, knowledgename: str, ispublic: bool):
        kid = self.getGuid()
        data = {
            "data": {
                "id": kid,
                "userid": userid,
                "knowledgename": knowledgename,
                "haschange": True,
                "ispublic": ispublic,
                "currentversion": "",
            }
        }
        self.Knowledgecollection.insert_one(data)
        return kid

    def get_knowledges(self, userid: str, containspublic: bool):
        if containspublic:
            query = {"$or": [{"data.userid": userid}, {"data.ispublic": True}]}
        else:
            query = {"data.userid": userid}
        # data = self.Knowledgecollection.find(query)
        # return [d["data"] for d in data]

        pipeline = [
            {"$match": query},
            {
                "$lookup": {
                    "from": "User",
                    "localField": "data.userid",
                    "foreignField": "data.id",
                    "as": "user_info",
                }
            },
            {
                "$unwind": {
                    "path": "$user_info",
                    "includeArrayIndex": "0",
                    "preserveNullAndEmptyArrays": True,
                }
            },
            {
                "$project": {
                    "id": "$data.id",
                    "userid": "$data.userid",
                    "username": "$user_info.data.username",
                    "knowledgename": "$data.knowledgename",
                    "haschange": "$data.haschange",
                    "ispublic": "$data.ispublic",
                    "currentversion": "$data.currentversion",
                }
            },
        ]
        data = self.Knowledgecollection.aggregate(pipeline)
        return [
            {key: value for key, value in item.items() if key != "_id"}
            for item in list(data)
        ]

    def get_knowledge_byid(self, knowledgeid: str):
        query = {"data.id": knowledgeid}
        data = self.Knowledgecollection.find_one(query)
        return data["data"]

    def edit_knowledge(self, knowledgeid: str, knowledge: dict):
        query = {"data.id": knowledgeid}
        newvalues = {"$set": {"data": knowledge}}
        self.Knowledgecollection.update_one(query, newvalues)

    def set_knowledge_haschange_true(self, knowledgeid: str):
        k = self.get_knowledge_byid(knowledgeid)
        k["haschange"] = True
        self.edit_knowledge(knowledgeid, k)

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
        self.set_knowledge_haschange_true(knowledgeid)

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
        self.set_knowledge_haschange_true(knowledgeid)

    def edit_qa(self, knowledgeid: str, qas: list[dict]):
        for qa in qas:
            query = {"$and": [{"data.knowledgeid": knowledgeid}, {"data.id": qa["id"]}]}
            newvalues = {
                "$set": {"data.q": qa["q"], "data.a": qa["a"], "data.e": qa["e"]}
            }
            self.QAcollection.update_one(query, newvalues)
        self.set_knowledge_haschange_true(knowledgeid)

    def add_new_session(self, userid: str, knowledgeid: str):
        sessionid = self.getGuid()
        data = {
            "data": {
                "id": sessionid,
                "userid": userid,
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

    def get_sessions(self, userid: str):
        query = {"$and": [{"data.userid": userid}, {"data.isdisabled": False}]}
        data = self.ChatSessioncollection.find(query)
        return [d["data"] for d in data]

    def get_session_byid(self, sessionid: str):
        query = {"data.id": sessionid}
        data = self.ChatSessioncollection.find_one(query)
        return data["data"]

    def edit_session(self, sessionid: str, session: dict):
        query = {"data.id": sessionid}
        newvalues = {"$set": {"data": session}}
        self.ChatSessioncollection.update_one(query, newvalues)

    def set_session_isdisabled_false(self, sessionid: str):
        s = self.get_session_byid(sessionid)
        s["isdisabled"] = False
        self.edit_knowledge(sessionid, s)
