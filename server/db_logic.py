import uuid
import os
import threading
import json
import copy


class MyCollection:
    def __init__(self, dir, name: str):
        self.lock = threading.Lock()
        self.Path = os.path.join(dir, name + ".json")
        if not os.path.exists(dir):
            os.mkdir(dir)
        if not os.path.exists(self.Path):
            self._save([])

    def select_all(self):
        return self._read()

    def insert_one(self, data):
        self.insert_many([data])

    def insert_many(self, data):
        ad = []
        for d in data:
            dbd = copy.deepcopy(d)
            dbd["id"] = str(uuid.uuid4())
            ad.append(dbd)
        alldata = self._read()
        alldata.extend(ad)
        self._save(alldata)

    def find_one(self, query):
        result = self.find(query)
        return result[0] if len(result) > 0 else None

    def find(self, query):
        data = self._read()
        return self._filter(data, query)

    def update_one(self, query, change):
        data = self.find_one(query)
        self._update_many([data], change)

    def update_many(self, query, change):
        data = self.find(query)
        self._update_many(data, change)

    def _update_many(self, data, change):
        if len(data) == 0:
            return
        for key, value in change["$set"].items():
            keys = key.split(".")
            for dd in data:
                d = dd
                for k in keys[:-1]:
                    d = d[k]
                d[keys[-1]] = value

        existids = [d["id"] for d in data]
        alldata = [d for d in self._read() if d["id"] not in existids]
        alldata.extend(data)
        self._save(alldata)

    def _and_filter(self, data, andarry):
        ids = set(item["id"] for item in data)
        for query in andarry:
            ids2 = set(item["id"] for item in self._filter(data, query))
            ids = ids & ids2
        return [item for item in data if item["id"] in ids]

    def _or_filter(self, data, orarry):
        combined_dict = {}
        for query in orarry:
            combined_dict.update(
                {item["id"]: item for item in self._filter(data, query)}
            )
        return list(combined_dict.values())

    def _filter(self, data, query):
        result = []
        for q in query.keys():
            if q == "$and":
                result = self._and_filter(data, query[q])
            elif q == "$or":
                result = self._or_filter(data, query[q])
            elif q == "$in":
                key, value = list(query.items())[0]
                keys = key.split(".")
                result = list(
                    filter(
                        lambda item: self._get_nested_value(item, keys) in value, data
                    )
                )
            else:
                key, value = list(query.items())[0]
                keys = key.split(".")
                if isinstance(value, dict):
                    result = list(
                        filter(
                            lambda item: self._get_nested_value(item, keys)
                            in value["$in"],
                            data,
                        )
                    )
                else:
                    result = list(
                        filter(
                            lambda item: self._get_nested_value(item, keys) == value,
                            data,
                        )
                    )
        return result

    def _get_nested_value(self, item, keys):
        for key in keys:
            item = item.get(key, None)
            if item is None:
                return None
        return item

    def _read(self):
        with self.lock:
            with open(self.Path, "r") as file:
                data = json.load(file)
        return data

    def _save(self, data):
        with self.lock:
            with open(self.Path, "w") as file:
                json.dump(data, file)


class DBLogic:
    def __init__(self, DbDir="C:\\db\\Chat"):
        self.host = DbDir
        self.Usercollection = self.get_col("User")
        self.Knowledgecollection = self.get_col("Knowledge")
        self.QAcollection = self.get_col("QA")
        self.ChatHistorycollection = self.get_col("ChatHistory")
        self.ChatSessioncollection = self.get_col("Session")

    def get_col(self, collection_name: str):
        return MyCollection(self.host, collection_name)

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

        data = self.Knowledgecollection.find(query)
        usermap = {}
        for u in self.Usercollection.select_all():
            usermap[u["data"]["id"]] = u["data"]["username"]
        result = [d["data"] for d in data]
        for d in result:
            d["username"] = usermap[d["userid"]]
        return result

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
        historyid = self.getGuid()
        data = {
            "data": {
                "id": historyid,
                "sessionid": sessionid,
                "q": q,
                "qtime": qtime,
                "a": a,
                "atime": atime,
                "pormpt": pormpt,
            }
        }
        self.ChatHistorycollection.insert_one(data)
        return historyid

    def get_chat_history_by_id(self, id: str):
        query = {"data.id": id}
        data = self.ChatHistorycollection.find_one(query)
        return data["data"]

    def chat_history_answer_by_id(self, id: str, answerjson: str):
        query = {"data.id": id}
        newvalues = {"$set": {"data.a": answerjson}}
        self.ChatHistorycollection.update_one(query, newvalues)

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
        query = {"data.id": sessionid}
        newvalues = {"$set": {"data.isdisabled": False}}
        self.ChatSessioncollection.update_one(query, newvalues)
