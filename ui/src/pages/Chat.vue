<template>
    <Navigator></Navigator>
    <div style="display: flex;">
        <div v-if="Sspage">
            <ListSession :sss="Sessions" :sid="SessionId" :ks="EnabledKnowledges" :shl="SessionHistory"
                @as="chatStore.AddSession" @ss="chatStore.SelectSession" @tc="tc"></ListSession>
        </div>
        <div v-else style="flex:1">
            <ListRecord :kn="kn" @ts="ts"></ListRecord>
        </div>
    </div>
</template>
<script name="management" setup lang="ts">
import ListRecord from '@/components/ListRecord.vue'
import ListSession from '@/components/ListSession.vue'
import Navigator from '@/components/Navigator.vue'
import { useChatStore } from '@/store/chat'
import { storeToRefs } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()
let Sspage = ref(true)
let chatStore = useChatStore()
let { Sessions, EnabledKnowledges, SessionId, SessionHistory, } = storeToRefs(chatStore)

Sspage.value = SessionId.value == undefined
function tc() {
    Sspage.value = false
}
function ts() {
    Sspage.value = true
}
function checkKnowledge() {
    let kcount = 0;
    EnabledKnowledges.value.forEach(k => {
        if (k.currentversion != "") {
            kcount++;
        }
    });
    if (kcount == 0) {
        router.replace({ name: "management" })
    }
}
function checkSession() {
    if (SessionId.value == undefined || SessionId.value == "") {
        ts()
    }
}
async function init() {
    await chatStore.init()
    checkKnowledge()
    checkSession()
}
onMounted(() => {
    init()
})
let kn = computed(() => {
    for (let s of Sessions.value) {
        if (s.sessionid == SessionId.value) {
            for (let k of EnabledKnowledges.value) {
                if (k.id == s.knowledgeid) {
                    return k.knowledgename
                }
            }
            return "not found"
        }
    }
}) 
</script>