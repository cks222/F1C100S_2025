import { defineStore } from 'pinia'
import { get, post } from '@/utils/axios'
import config from '@/config';
import { type Session, type Knowledge, type Message, type SessionHistory } from '@/types';

export const useChatStore = defineStore('Chat', {
    actions: {
        async init() {
            await this.GetSessions()
            await this.GetEnabledKnowledges()

            let sexist = false
            for (let s of this.Sessions) {
                if (s.sessionid == this.SessionId) {
                    sexist = true
                }
            }
            if (!sexist) {
                this.SelectSession("")
            }
        },
        async GetSessions() {
            const result = await get(config.api.get.sessions + "?username=" + this.UserName)
            this.Sessions = result.data
            await this.GetSessionHistory()
        },
        async GetEnabledKnowledges() {
            const result = await get(config.api.get.knowledges + "?username=" + this.UserName + "&containspublic=true")
            this.EnabledKnowledges = result.data
        },
        SelectSession(sessionid: string) {
            localStorage.setItem("sessionid", sessionid)
            this.SessionId = sessionid
        },
        async GetSessionHistory() {
            this.SessionHistory = []
            this.Sessions.forEach(async (x: any) => {
                const result = await get(config.api.get.history + "?sessionid=" + x.sessionid)
                let history = <SessionHistory>{ SessionId: x.sessionid, Messages: [] }
                result.data.forEach((y: any, z: number) => {
                    history.Messages.push({ Role: "user", Content: y["q"], Time: y["qtime"] })
                    history.Messages.push({ Role: "assistant", Content: y["a"], Time: y["atime"] })
                })
                this.SessionHistory.push(history)
            })
        },
        async AddSession(knowledgeid: string) {
            let path = config.api.get.add_session + "?username=" + this.UserName + "&knowledgeid=" + knowledgeid
            let response = await get(path)
            this.SessionId = response.data
            await this.GetSessions()
            this.SelectSession(this.SessionId)
        },
        async SendMessage() {
            let sid=`${this.SessionId}`
            this.ErrorMessages = ""
            if (this.Question == "") {
                this.ErrorMessages = "Please input question"
                return
            }
            if (this.State == this.State_Sent) {
                this.ErrorMessages = "Please waitting for the answer"
                return
            }
            this.State = this.State_Sent
            var formData = new FormData();
            let Messages = <Message[]>[]
            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    Messages = x.Messages
                }
            })
            formData.append("history", JSON.stringify(Messages));
            formData.append("question", this.Question);
            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    x.Messages.push({ Role: "user", Content: this.Question, Time: "" })
                }
            })
            const result = await post(`${config.api.post.chat}?sessionid=${sid}`, formData)

            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    x.Messages[x.Messages.length - 1] = { Role: "user", Content: result.data["q"], Time: result.data["qtime"] }
                    x.Messages.push({ Role: "assistant", Content: result.data["a"], Time: result.data["atime"] })
                }
            })
            this.Question = ""
            this.State = this.State_Anwserd
        }
    },
    state() {
        return {
            UserName: <string>localStorage.getItem("userName"),
            SessionId: <string>localStorage.getItem("sessionid"),
            Sessions: <Session[]>[],
            EnabledKnowledges: <Knowledge[]>[],
            SessionHistory: <SessionHistory[]>[],
            Question: "",
            ErrorMessages: "",

            State: "Y",
            State_Sent: "X",
            State_Anwserd: "Y",
        }
    }
})