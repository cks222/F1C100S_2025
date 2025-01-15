import { defineStore } from 'pinia'
import {
    api_sessions, api_add_sessions, api_del_sessions, get_api_knowledges, api_history, api_chat
} from '@/utils/axios'
import config from '@/config';
import { type Session, type Knowledge, type Message, type SessionHistory, type AssistantAnswer, type AssistantQA } from '@/types';


export const useChatStore = defineStore('Chat', {
    actions: {
        async init() {
            this.UserId = <string>localStorage.getItem("userid")
            this.SessionId = <string>localStorage.getItem("sessionid")
            await this.GetSessions()
            await this.GetEnabledKnowledges()

            let sexist = false
            for (let s of this.Sessions) {
                if (s.id == this.SessionId) {
                    sexist = true
                }
            }
            if (!sexist) {
                this.SelectSession("")
            }
        },
        async GetSessions() {
            const data = await api_sessions(this.UserId)
            this.Sessions = data
            await this.GetSessionHistory()
        },
        async DelSession(sessionid: string) {
            const data = await api_del_sessions(sessionid)
            return data
        },
        async GetEnabledKnowledges() {
            const data = await get_api_knowledges(this.UserId, true)
            this.EnabledKnowledges = data
        },
        SelectSession(sessionid: string) {
            localStorage.setItem("sessionid", sessionid)
            this.SessionId = sessionid
        },
        async GetSessionHistory() {
            this.SessionHistory = []
            this.Sessions.forEach(async (x: any) => {
                const data = await api_history(x.id)
                let history = <SessionHistory>{ SessionId: x.id, Messages: [] }
                data.forEach((y: any, z: number) => {
                    history.Messages.push({ Role: "user", Content: y["q"], Time: y["qtime"] })
                    let _aa = JSON.parse(y['a'])
                    let aa = <AssistantAnswer>{
                        useLLM: _aa.useLLM,
                        text: _aa.text,
                        jsontext: <AssistantQA[]>JSON.parse(_aa.jsontext)
                    }

                    history.Messages.push({ Role: "assistant", Content: y['a'], AssistantAnswer: aa, Time: y["atime"] })
                })
                this.SessionHistory.push(history)
            })
        },
        async AddSession(knowledgeid: string) {
            let data = await api_add_sessions(this.UserId, knowledgeid)
            this.SessionId = data
            await this.GetSessions()
            this.SelectSession(this.SessionId)
        },
        async SendMessage() {
            let sid = `${this.SessionId}`
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
            let Messages = <Message[]>[]
            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    Messages = x.Messages
                }
            })
            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    x.Messages.push({ Role: "user", Content: this.Question, Time: "" })
                }
            })
            const data = await api_chat(sid, JSON.stringify(Messages), this.Question)

            this.SessionHistory.forEach(x => {
                if (x.SessionId == sid) {
                    x.Messages[x.Messages.length - 1] = { Role: "user", Content: data["q"], Time: data["qtime"] }
                    let _aa = JSON.parse(data['a'])
                    let aa = <AssistantAnswer>{
                        useLLM: _aa.useLLM,
                        text: _aa.text,
                        jsontext: <AssistantQA[]>JSON.parse(_aa.jsontext)
                    }
                    x.Messages.push({ Role: "assistant", Content: data["a"], AssistantAnswer: aa, Time: data["atime"] })
                }
            })
            this.Question = ""
            this.State = this.State_Anwserd
            this.ErrorMessages = ""
        }
    },
    state() {
        return {
            UserId: <string>localStorage.getItem("userid"),
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