import { defineStore } from 'pinia'
import {
    get_api_addknowledges, post_api_updateknowledge, api_upload_file, get_api_qas, post_api_qa, get_publish_knowledge, get_api_knowledges
} from '@/utils/axios'
import { type Knowledge, type KQA, type QA } from '@/types'

export const useKnowledgeStore = defineStore('Knowledge', {
    actions: {
        async init() {
            this.UserId = <string>localStorage.getItem("userid")
            return this.GetUserKnowledges()
        },
        async AddKnowledge(knowledgename: string, ispublic: boolean) {
            let data = await get_api_addknowledges(this.UserId, knowledgename, ispublic)
            this.GetUserKnowledges()
            return data
        },
        async updateKnowledge(knowledgeid: string, k: Knowledge) {
            await post_api_updateknowledge(knowledgeid, JSON.stringify(k))
            this.GetUserKnowledges()
        },
        async upload_file(knowledgeid: string, data: FormData) {
            await api_upload_file(knowledgeid, data)
            this.SetHasChange(knowledgeid, true)
        },
        async GetQA(knowledgeid: string) {
            let totalcount = 0
            let start = 0, count = 30
            let data = <QA[]>[]
            this.QA = { knowledgeid: knowledgeid, QAS: [] }
            do {
                data = await get_api_qas(knowledgeid, start, count)
                if (this.QA.knowledgeid != knowledgeid) {
                    return 0
                }
                this.QA.QAS = this.QA.QAS.concat(data)
                totalcount += data.length
                start += count
            } while (data.length == count)
            return totalcount
        },
        async RemoveQA(knowledgeid: string, qas: string) {
            await post_api_qa(knowledgeid, "remove", qas)
            await this.GetQA(knowledgeid)
            this.SetHasChange(knowledgeid, true)
        },
        async PublishKnowledge(knowledgeid: string) {
            await get_publish_knowledge(knowledgeid)
            this.GetUserKnowledges()
        },
        async GetUserKnowledges() {
            const data = await get_api_knowledges(this.UserId, true)
            this.UserKnowledges = []
            data.forEach((k: Knowledge) => {
                if (k.currentversion != "") {
                    this.UserKnowledges.push(k)
                }
            });
            this.UserKnowledges = data
        },
        async SetHasChange(knowledgeid: string, haschange: boolean) {
            this.UserKnowledges.forEach(k => {
                if (k.id == knowledgeid) {
                    k.haschange = haschange
                }
            })
        }
    },
    state() {
        return {
            UserId: <string>localStorage.getItem("userid"),
            UserKnowledges: <Knowledge[]>[],
            UserIdName: <Knowledge[]>[],
            QA: <KQA>{},
        }
    }
})