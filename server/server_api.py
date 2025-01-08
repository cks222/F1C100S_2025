from mongo_logic import MongoLogic
from datetime import datetime
from emb_model import MyEmbModel
from emb_db import MyMilvusClient, MyMilvusData
from Phi3 import Phi
#from llama31b import Llama321b
import json


class API:
    def __init__(self):
        self.ml = MongoLogic()
        self.llm = Phi()
        self.emb = MyEmbModel()
        self.embdb = MyMilvusClient()

    def ToEmb(self, sentence):
        return self.emb.to_emb(sentence)[0]

    def Chat(self, messages):
        #return self.llm.Chat(messages)
        return "I am a chatbot, and I need to summarize the answers based on the user's' found some similar qa 'in order to answer their questions"

    def GetSimilaryQ(self, knowledgeid, question):
        category = self.ml.get_knowledge_byid(knowledgeid)["currentversion"]
        vector = self.ToEmb(question)
        return self.embdb.search_similar(
            category=knowledgeid + category, vector=vector, top_k=3
        )

    def api_login(self, username: str, encrypted_str: str):
        if self.ml.get_user(username, encrypted_str) == "":
            return "no match user"
        return username

    def api_hasuser(self, username: str):
        return self.ml.has_user(username)

    def api_signup(self, username: str, encrypted_str: str):
        self.ml.add_user(username, encrypted_str)
        return username

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

    def get_api_knowledges(self, username: str, containspublic: bool):
        return self.ml.get_knowledges(username, containspublic)

    def get_api_addknowledges(self, username: str, knowledgename, ispublic: bool):
        return self.ml.add_knowledge(username, knowledgename, ispublic)

    def post_api_updateknowledge(self, knowledgeid: str, knowledge: dict):
        return self.ml.edit_knowledge(knowledgeid, knowledge)

    def get_api_qas(self, knowledgeid: str):
        return self.ml.get_qas(knowledgeid)

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

    def combine_chatpormpt(self, sessionid: str, chathistory: str, question: str):
        s = self.ml.get_sessions_byid(sessionid)
        prompt = [
            {
                "role": "system",
                "content": "You are a chatbot, and you need to summarize the answers based on the user's' found some similar qa 'in order to answer their questions",
            }
        ]
        sq = self.GetSimilaryQ(s["knowledgeid"], question)
        '''
        if chathistory != "":
            for h in json.loads(chathistory):
                prompt.append(
                    {
                        "role": h.get("role", h.get("Role", "")),
                        "content": h.get("content", h.get("Content", "")),
                    }
                )
        '''
        qa = ""
        if len(sq) > 0:
            for q in sq:
                qa += "question:"+q["question"] +"\nanswer:"+ q["answer"] + "\n"
        prompt.append(
            {"role": "user", "content": "I found some similar questions:" + qa}
        )
        prompt.append({"role": "user", "content": question})
        return prompt

    def api_chat(self, sessionid: str, history, question: str):
        sid = sessionid
        qtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = self.combine_chatpormpt(sid, history, question)
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
                MyMilvusData(
                    category=category, vector=qa["e"], question=qa["q"], answer=qa["a"]
                )
            )
        self.embdb.insert_data(data)
        self.ml.edit_knowledge(knowledgeid, knowledge)

    def api_sessions(self, username: str):
        return self.ml.get_sessions(username)

    def get_publish_knowledge(self, knowledgeid: str):
        version = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        mgdata = self.ml.get_qas(knowledgeid)
        data = []
        for d in mgdata:
            data.append(
                MyMilvusData(
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

    def api_add_sessions(self, username: str, knowledgeid: str):
        return self.ml.add_new_session(username, knowledgeid)
