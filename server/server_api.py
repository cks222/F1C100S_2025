from typing import List
from mongo_logic import MongoLogic
from datetime import datetime
from emb_model import MyEmbModel
from chat_model import MyChatModel
from emb_db import MyMilvusClient
import json


class API:
    def __init__(self):
        self.usellm = False
        self.ml = MongoLogic()
        self.llm = MyChatModel()
        self.emb = MyEmbModel()
        self.embdb = MyMilvusClient()

    def ToEmb(self, sentence):
        return self.emb.to_emb(sentence)[0]

    def Chat(self, messages):
        return self.llm.Chat(messages)

    def GetSimilaryQ(self, knowledgeid, question):
        category = self.ml.get_knowledge_byid(knowledgeid)["currentversion"]
        vector = self.ToEmb(question)
        return self.embdb.search_similar(
            category=knowledgeid + category, vector=vector, top_k=3
        )

    def api_login(self, account: str, encrypted_str: str):
        if self.ml.login(account, encrypted_str) == "":
            return "no match user"
        return account

    def api_login_byid(self, userid: str, encrypted_str: str):
        if self.ml.login_by_id(userid, encrypted_str) == "":
            return "no match user"
        return userid

    def api_getuser_byid(self, userid: str):
        return self.ml.get_user_by_id(userid)

    def api_has_account(self, account: str):
        return self.ml.api_has_account(account)

    def api_signup(self, account: str, encrypted_str: str):
        return self.ml.add_user(account, encrypted_str)

    def api_upload_file(self, knowledgeid: str, content: str):
        qas = []
        for line in content.split("\n"):
            if line.strip() != "":
                qa = json.loads(line)
                q = qa.get("q", qa.get("question", ""))
                a = qa.get("a", qa.get("answer", ""))
                e = qa.get("e", qa.get("embedding", self.ToEmb(q)))
                qas.append({"q": q, "a": a, "e": e.tolist()})
        self.ml.add_qas(knowledgeid, qas)

    def get_api_knowledges(self, userid: str, containspublic: bool):
        return self.ml.get_knowledges(userid, containspublic)

    def get_api_addknowledges(self, userid: str, knowledgename, ispublic: bool):
        return self.ml.add_knowledge(userid, knowledgename, ispublic)

    def post_api_updateknowledge(self, knowledgeid: str, knowledge: dict):
        return self.ml.edit_knowledge(knowledgeid, knowledge)

    def get_api_qas(self, knowledgeid: str):
        return [
            {
                "id": qa["id"],
                "isdisabled": qa["isdisabled"],
                "knowledgeid": qa["knowledgeid"],
                "a": qa["a"],
                "q": qa["q"],
            }
            for qa in self.ml.get_qas(knowledgeid)
        ]

    def post_api_qa(self, knowledgeid: str, method: str, qas: str):
        qas = json.loads(qas)
        if method == "new":
            nqas = [
                {
                    "q": qa.get("q", qa.get("question", "")),
                    "a": qa.get("a", qa.get("answer", "")),
                    "e": qa.get(
                        "e",
                        qa.get(
                            "embedding", self.ToEmb(qa.get("q", qa.get("question", "")))
                        ),
                    ),
                }
                for qa in qas
            ]
            self.ml.add_qas(knowledgeid, nqas)
        elif method == "remove":
            qaids = [qa["id"] for qa in qas]
            self.ml.remove_qa(knowledgeid, qaids)
        elif method == "edit":
            eqas = [
                {
                    "q": qa.get("q", qa.get("question", "")),
                    "a": qa.get("a", qa.get("answer", "")),
                    "e": qa.get(
                        "e",
                        qa.get(
                            "embedding", self.ToEmb(qa.get("q", qa.get("question", "")))
                        ),
                    ),
                }
                for qa in qas
            ]
            self.ml.edit_qa(knowledgeid, eqas)
        else:
            pass

    def api_history(self, sessionid: str):
        return self.ml.get_chat_history(sessionid)

    def combine_chatpormpt(self, sq: List, chathistory: str, question: str):

        prompt = [
            {
                "role": "system",
                "content": "You are a chatbot, and you need to summarize the answers based on the user's' found some similar qa 'in order to answer their questions",
            }
        ]
        """
        if chathistory != "":
            for h in json.loads(chathistory):
                prompt.append(
                    {
                        "role": h.get("role", h.get("Role", "")),
                        "content": h.get("content", h.get("Content", "")),
                    }
                )
        """
        qa = ""
        if len(sq) > 0:
            for q in sq:
                qa += "question:" + q["question"] + "\nanswer:" + q["answer"] + "\n"
        prompt.append(
            {"role": "user", "content": "I found some similar questions:" + qa}
        )
        prompt.append({"role": "user", "content": question})
        return prompt

    def api_chat(self, sessionid: str, history, question: str):
        sid = sessionid
        qtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s = self.ml.get_session_byid(sid)
        sq = self.GetSimilaryQ(s["knowledgeid"], question)
        prompt = self.combine_chatpormpt(sq, history, question)
        a = sq[0]["answer"]
        if self.usellm:
            a = self.Chat(prompt)
        atime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ml.add_new_history(sid, question, qtime, a, atime, prompt)
        return {"sessionid": sid, "q": question, "qtime": qtime, "a": a, "atime": atime}

    def api_build_knowledge(self, knowledgeid: str):
        qas = self.ml.get_qas(knowledgeid)
        knowledge = self.ml.get_knowledge_byid(knowledgeid)
        knowledge["currentversion"] = self.ml.getGuid()
        self.ml.edit_knowledge(knowledgeid, {"currentversion": +1})
        category = knowledge["currentversion"]
        data = []
        for qa in qas:
            data.append(
                self.embdb.build_data(
                    category=category, vector=qa["e"], question=qa["q"], answer=qa["a"]
                )
            )
        self.embdb.insert_data(data)
        self.ml.edit_knowledge(knowledgeid, knowledge)

    def api_sessions(self, userid: str):
        return self.ml.get_sessions(userid)

    def get_publish_knowledge(self, knowledgeid: str):
        version = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        mgdata = self.ml.get_qas(knowledgeid)
        data = []
        for d in mgdata:
            data.append(
                self.embdb.build_data(
                    category=knowledgeid + version,
                    vector=d["e"],
                    question=d["q"],
                    answer=d["a"],
                )
            )
        self.embdb.insert_data(data)
        knowledge = self.ml.get_knowledge_byid(knowledgeid)
        knowledge["currentversion"] = version
        knowledge["haschange"] = False
        return self.ml.edit_knowledge(knowledgeid, knowledge)

    def api_add_sessions(self, userid: str, knowledgeid: str):
        return self.ml.add_new_session(userid, knowledgeid)

    def disable_session(self, sessionid: str):
        return self.ml.set_session_isdisabled_false(sessionid)
