<template>
    <div>
        <div class="sidebar" >
            <div class="content" @click="emit('h')">
                <div></div>
                <div></div>
            </div>
            <div class="mylink">
                <div :class="{ 'actcls': 'chat' == actr }" @click="skip('chat')">Chat</div>
            </div>
            <div class="mylink">
                <div :class="{ 'actcls': 'management' == actr }" @click="skip('management')">Knowledge</div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">

import { ref,defineEmits,defineProps } from 'vue'
import { useRouter } from 'vue-router'

const prop=defineProps({
    "ih":{
        type:Boolean,
        default:true
    }
})
const emit=defineEmits(["s","h"])

const r = useRouter()
let actr = ref("")
function skip(rname: string) {
    if (actr.value == rname || rname==""){
        return
    }
    actr.value = rname
    r.push({ name: rname })
}
</script>
<style lang="css" scoped>
.sidebar {
    background-color: rgb(132, 157, 180);
    width: 100%;
    transition: transform 0.3s ease;
    height: 100vh;
}

.sidebar.is-hidden {
    transform: translateX(-100%);
}

.content {
    display: flex;
    justify-content: right;
    padding-top: 20px;
}

.content>div:last-child {
    text-align: center;
    width: 20px;
}

.content>div:first-child::after {
    content: '';
    display: inline-block;
    height: 0px;
    width: 0px;
    border-top: 10px solid transparent;
    border-right: 14px solid transparent;
    border-bottom: 10px solid transparent;
    margin: 6px 6px 3px 6px;
}

.sidebar:hover>.content>div:first-child {
    background-color: transparent;
    border-radius: 10px;
}

.sidebar:hover>.content>div:first-child::after {
    border-right: 14px solid gray;
}

.sidebar:hover>.content>div:first-child:hover {
    cursor: pointer;
}

.sidebar:hover>.content>div:first-child:hover::after {
    cursor: pointer;
    border-right: 14px solid black;
}


.sidebar>div:nth-child(2) {
    margin-top: 140px;
}

.mylink {
    margin-top: 5px;
    padding-left: 60px;
    text-decoration: none;
    color: black;
    font-weight: bold;
}

.mylink>div {
    display: inline-block;
    padding: 4px 10px 4px 10px;
    width: 210px;
    cursor: pointer;
}

.mylink>div:hover {
    border-radius: 8px;
    background-color: gainsboro;
}
.actcls{
    border-radius: 8px;
    background-color: grey!important;
    cursor: inherit!important;
}
*{
    user-select: none;
}
</style>