<template>
    <div class="km">
        <div>
            <div class="content">
                <div style="font-size: 30px;font-weight: bold;">
                    🦜 Chat
                </div>
                <div>
                    <select class="selectk" v-model="knowledgeid" @change="selectSession">
                        <option v-for="k of EnabledKnowledges" :value="k.id">{{ k.knowledgename }}</option>
                    </select>
                    <div v-if="MessageHistory.length > 0" class="refresh" @click="clearSession"
                        title="clear chat history">♻</div>
                </div>
                <div>
                    <div ref="mh" style="overflow-y: auto;" :style="{ 'height': listh + 'px' }">
                        <div v-for="s in MessageHistory" :class="s.Role">
                            <div v-if="s.Role == 'assistant'" class="head">
                                <div>🤖</div>
                            </div>
                            <div v-if="s.Role == 'user'" class="head">
                                <div>🧑‍🦱</div>
                            </div>
                            <div class="hc">
                                <div v-if="s.Role == 'user'">{{ s.Content }}</div>
                                <div v-if="s.Role == 'assistant' && s.AssistantAnswer.useLLM">
                                    <div class="SimQA">
                                        <div class="xiala"></div>
                                        <div class="qa qax" style="text-align: center;font-weight: bold;">
                                            <div>question</div>
                                            <div>answer</div>
                                        </div>
                                        <div v-for="qa of s.AssistantAnswer.jsontext" class="qa qax">
                                            <div>{{ qa.question }}</div>
                                            <div>{{ qa.answer }}</div>
                                        </div>
                                        <br>
                                        <hr>
                                        <br>
                                    </div>
                                    
                                    {{ s.AssistantAnswer.text }}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div style="height: 20px;margin-top:10px;">
                        <div style="color: red;">{{ ErrorMessages }}</div>
                    </div>
                    <div class="userpannel">
                        <textarea rows="1" v-model="Question" @keyup.enter.prevent="chatStore.SendMessage"></textarea>
                        <div class="btn sendbtn" @click="chatStore.SendMessage"><svg viewBox="0 0 24 24"
                                aria-hidden="true" focusable="false" fill="currentColor"
                                xmlns="http://www.w3.org/2000/svg" color="inherit"
                                class="e14lo1l1 st-emotion-cache-qsoh6x ex0cdmw0">
                                <rect width="24" height="24" fill="none"></rect>
                                <path
                                    d="M3 5.51v3.71c0 .46.31.86.76.97L11 12l-7.24 1.81c-.45.11-.76.51-.76.97v3.71c0 .72.73 1.2 1.39.92l15.42-6.49c.82-.34.82-1.5 0-1.84L4.39 4.58C3.73 4.31 3 4.79 3 5.51z">
                                </path>
                            </svg></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useChatStore } from '@/store/chat'
import { storeToRefs } from 'pinia'
import { computed, onMounted, ref, watch, nextTick } from 'vue'
const chatStore = useChatStore()
let { Sessions, EnabledKnowledges, SessionId, SessionHistory, State,   ErrorMessages, Question } = storeToRefs(chatStore)
let knowledgeid = ref("")
let mh = ref()
let MessageHistory = computed(() => {
    for (let sh of SessionHistory.value) {
        if (sh.SessionId == SessionId.value) {
            return sh.Messages
        }
    }
    return []
})
watch(() => {
    for (let sh of SessionHistory.value) {
        if (sh.SessionId == SessionId.value) {
            let xx=""
            sh.Messages.slice(-5).forEach(x => xx += "|"+ x.Content.length);
            console.log(xx)
            return xx
        }
    }
    return "[]"
}, () => {
    nextTick(() => { mh.value.scrollTop = mh.value.scrollHeight; });
})
watch(State, () => {
    nextTick(() => { mh.value.scrollTop = mh.value.scrollHeight; });
})
async function clearSession() {
    await chatStore.DelSession(SessionId.value)
    await chatStore.AddSession(knowledgeid.value)
    await chatStore.GetSessionHistory()
}
function selectSession() {
    let notselect = true;
    for (let s of Sessions.value) {
        if (s.knowledgeid == knowledgeid.value) {
            chatStore.SelectSession(s.id)
            notselect = false;
        }
    }
    if (notselect) {
        chatStore.AddSession(knowledgeid.value)
    }
}
onMounted(async () => {
    await chatStore.init()
    for (let s of Sessions.value) {
        if (s.id == SessionId.value) {
            knowledgeid.value = s.knowledgeid
        }
    }
})
let listh = computed(() => {
    let height = document.documentElement.scrollHeight;
    let result = height - 288;
    return result <= 100 ? 100 : result;
})
</script>
<style scoped>
.km {
    display: flex;
    justify-content: center;
}

.km>div {
    min-width: 800px;
    width: 80%;
}

.content {
    width: 100%;
}

.content>div {
    margin-top: 25px;
}

.userpannel {
    border-radius: 5px;
    border: 1px solid transparent;
    background-color: #F0F2F6;
    display: flex;
}

.userpannel>textarea {
    flex: 1;
    background-color: transparent;
    border-color: transparent;
    resize: none;
    padding-top: 12px;
    font-size: 20px;
    line-height: 15px;
    padding-left: 15px;
}

.userpannel>textarea:focus {
    outline: none;
    border-color: transparent !important;
}

.sendbtn {
    width: 40px;
    height: 40px;
}

.assistant,
.user {
    display: flex;
    margin-top: 10px;
    padding: 10px;
}

.user {
    background-color: lightgoldenrodyellow;
    border-radius: 5px;
}

.head {
    font-size: 25px;
    user-select: none;
}

.hc {
    white-space: pre-wrap;
    padding-top: 10px;
    margin-left: 10px;
}

.refresh {
    display: inline-block;
    font-size: 30px;
    cursor: pointer;
    text-align: center;
    width: 50px;
}

.refresh:hover {
    color: red;
}


.qax {
    border: 1px solid #F0F2F6;
    font-size: 13px;
    padding: 1px;
    line-height: 20px;
}

.qax>div:first-child {
    border-right: 1px solid #F0F2F6;
}

.qax:nth-child(2n) {
    background-color: azure;
}

.qax:nth-child(2n+1) {
    background-color: white;
}

.qa {
    display: flex;
    justify-content: left;
}



.qa>div:first-child {
    flex: 3;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    padding: 5px;
}

.qa>div:last-child {
    flex: 4;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    padding: 5px;
}
.SimQA{
    height: 12px;
    overflow: hidden;
}
.SimQA:hover{
    animation: showxiala 1s forwards;
}
.xiala{
    height: 10px;
    text-align: center;
    color: white;
    animation: kfxiala 30s infinite;
    border-radius: 5px;
    align-items: center;
    display: flex;
    justify-content: center;
}
.xiala::before{
    height: 0px;
    width:  0px;
    display: inline-block;
    content: '';
    border-top:8px solid gray;
    border-left:10px solid transparent;
    border-right:10px solid transparent;
}
.SimQA:hover>.xiala{
    display: none;
}
@keyframes showxiala {
    0% {
        height: 10px;
    }
    50% {
        height: 70px;
    }
    100% {
        height: auto;
    }
}@keyframes kfxiala {
    0%,100% {        
        background-color: white;
        border:1px solid gainsboro
    }
    50% {
        background-color: gainsboro;
        border:1px solid gray
    } 
}
</style>