<template>
    <div style="display: flex;justify-content: center;">
        <div style="width:780px;border:1px solid black;padding: 10px;margin-top: 10px;">
            <div style="display: flex;justify-content: space-between;">
                <div>Knowledge:{{ prop.kn }}</div>
                <div class="btn initbtn" @click="emit('ts')">Select Session</div>
            </div>
            <hr>
            <div style="height: 600px;overflow-y: scroll;">
                <div v-for="s, d in MessageHistory" :class="s.Role">
                    <div v-if="s.Role == 'assistant'" class="head">
                        <div>AI</div>
                    </div>
                    <div v-if="s.Role == 'assistant'" class="space">
                    </div>
                    <div>
                        <div style="height: 20px;background-color: transparent;">
                        </div>
                        <div class="content">
                            <div>{{ s.Content }}</div>
                        </div>
                    </div>

                    <div v-if="s.Role == 'user'" class="space">
                    </div>
                    <div v-if="s.Role == 'user'" class="head">
                        <div>我</div>
                    </div>
                </div>


                <div v-if="State == State_Sent" class="assistant">
                    <div class="head">
                        <div>AI</div>
                    </div>
                    <div class="space">
                    </div>
                    <div>
                        <div style="height: 20px;background-color: transparent;">
                        </div>
                        <div class="content">
                            <div>
                                loading . . .</div>
                        </div>
                    </div>
                </div>
            </div>
            <hr>
            <div class="userpannel">
                <textarea v-model="Question" @keyup.enter="chatStore.SendMessage"></textarea>
                <div class="btn sendbtn" @click="chatStore.SendMessage">发送</div>
            </div>
            <div v-if="ErrorMessages!=''" class="userpannel">
                <div style="color: red;">{{ ErrorMessages }}</div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { useChatStore } from '@/store/chat'
import { storeToRefs } from 'pinia'
import { computed, defineProps, defineEmits } from 'vue'

let emit = defineEmits(["ts"])
let prop = defineProps({ "kn": { type: String, default: "" } })


let chatStore = useChatStore()
let { SessionHistory, State, State_Sent, Question, SessionId,ErrorMessages } = storeToRefs(chatStore)

let MessageHistory = computed(() => {
    for (let x of SessionHistory.value) {
        if (x.SessionId == SessionId.value) {
            return x.Messages
        }
    }
    return []
})

chatStore.init()
</script>
<style scoped>
.user,
.assistant {
    display: flex;
    align-items: start;
}

.user .content>div {
    background-color: cadetblue;
    padding: 5px;
    border-radius: 5px;
}

.assistant .content>div {
    background-color: gainsboro;
    padding: 5px;
    border-radius: 5px;
}

.assistant>div:last-child,
.user>div:first-child {
    flex: 1;
}

.user .content {
    display: flex;
    justify-content: right;
    white-space: pre-wrap;
}

.assistant .content {
    display: flex;
    justify-content: left;
    align-items: center;
    white-space: pre-wrap;
}

.content>div:first-child {
    max-width: 600px;
    word-wrap: break-word;
}

.btn {
    background-color: antiquewhite;
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
}

.btn:hover {
    background-color: lightcyan;
}

.sendbtn {
    font-size: 25px;
    width: 60px;
    height: 30px;
    padding: 10px;
}

.initbtn {
    padding: 3px;
}

.userpannel {
    margin-top: 10px;
    display: flex;
    justify-content: space-around;
    align-items: center;
}

.userpannel>textarea {
    flex: 1;
    height: 50px;
}

.head {
    width: 40px;
    height: 40px;
    border-radius: 100px;
    border: 1px solid black;
    display: flex;
    align-items: center;
    justify-content: center;
}

.space {
    width: 10px;
}
</style>