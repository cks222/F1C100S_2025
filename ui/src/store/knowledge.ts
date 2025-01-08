import { defineStore } from 'pinia'
import { get, post, postfile } from '@/utils/axios'
import { type Knowledge, type KQA } from '@/types'
import config from '@/config'

export const useKnowledgeStore = defineStore('Knowledge', {
    actions: {
        async init() {
            return this.GetUserKnowledges()
        },
        async AddKnowledge(knowledgename: string, ispublic: boolean) {
            let path = config.api.get.add_knowledges + "?username=" + this.UserName + "&knowledgename=" + knowledgename + "&ispublic=" + ispublic
            let response = await get(path)
            this.GetUserKnowledges()
            return response.data
        },
        async updateKnowledge(knowledgeid: string, k: Knowledge) {
            let fd = new FormData()
            fd.append("knowledge", JSON.stringify(k))
            let path = config.api.post.updateknowledge + "?knowledgeid=" + knowledgeid
            await post(path, fd)
            this.GetUserKnowledges()
        },
        async upload_file(knowledgeid: string, data: FormData) {
            let path = config.api.post.upload_file + "?knowledgeid=" + knowledgeid
            await postfile(path, data)
            this.SetHasChange(knowledgeid,true)
        },
        async GetQA(knowledgeid: string) {
            let totalcount = 0
            let start = 0, count = 30
            let result = await get(config.api.get.qas + "?knowledgeid=" + knowledgeid + "&start=" + start + "&count=" + count)
            this.QA = { knowledgeid: knowledgeid, QAS: [] }
            this.QA.QAS = [].concat(result.data)
            totalcount += result.data.length
            while (result.data.length == count) {
                start += count
                result = await get(config.api.get.qas + "?knowledgeid=" + knowledgeid + "&start=" + start + "&count=" + count)
                this.QA.QAS = this.QA.QAS.concat(result.data)
                totalcount += result.data.length
            }
            return totalcount
        },
        async RemoveQA(knowledgeid: string, data: FormData) {
            let path = config.api.post.qa + "?method=remove&knowledgeid=" + knowledgeid
            await postfile(path, data)
            await this.GetQA(knowledgeid)
            this.SetHasChange(knowledgeid,true)
        },
        async PublishKnowledge(knowledgeid: string) {
            let path = config.api.get.publish_knowledge + "?knowledgeid=" + knowledgeid
            await get(path)
            this.GetUserKnowledges()
        },
        async GetUserKnowledges() {
            const result = await get(config.api.get.knowledges + "?username=" + this.UserName + "&containspublic=false")
            this.UserKnowledges = result.data
        },
        async SetHasChange(knowledgeid: string,haschange:boolean){
            this.UserKnowledges.forEach(k=>{
                if(k.id==knowledgeid){
                    k.haschange=haschange
                }
            })
        }
    },
    state() {
        return {
            UserName: <string>localStorage.getItem("userName"),
            UserKnowledges: <Knowledge[]>[],
            QA: <KQA>{},
        }
    }
})