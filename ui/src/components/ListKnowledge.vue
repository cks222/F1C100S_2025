<template>

    <div :class='{"k":true,"ck":k.id==cid}' v-for="k in uks" :key="k.id">
        <div class="kfl">
            <div>Name:</div>
            <div>{{ k.knowledgename }}</div>
        </div>
        <div :class="{'ksl':true,'np':k.currentversion==''}">
            <div>Last publish:</div>
            <div>{{ k.currentversion }}</div>
        </div>
        <div class="ktl">

            <div @click="publick(k.id, k)">
                <div :class="{ 'publicak': k.ispublic }">Public</div>
                <div :class="{ 'publicak': !k.ispublic }">Private</div>
            </div>
            <div class="btn" @click="eqa(k.id)">Edit QA</div>
            <div class="btn" @click="publishk(k.id)">Publish</div>
        </div>
    </div>

    <div v-if="!showAddNew" class="k">
        
        <div class="ktl">
            <div >
            </div>
            <div class="btn" @click="showAddNew=!showAddNew">Add New</div>
        </div>
    </div>
    <div v-if="showAddNew" class="k">
        <div class="kfl">
            <div>New Name:</div>
            <div>
                <input type="text" v-model="knowledgename">
            </div>
        </div>
        <div class="ksl">
            <div>&nbsp;</div>
            <div> </div>
        </div>
        <div class="ktl">
            <div @click="ispublic = !ispublic">
                <div :class="{ 'publicak': ispublic }">Public</div>
                <div :class="{ 'publicak': !ispublic }">Private</div>
            </div>
            <div class="btn" @click="addk">Add New</div>
        </div>
    </div>
</template>
<script name="klist" setup lang="ts">
import { defineProps, defineEmits, ref } from 'vue'
import { type Knowledge } from '@/types'

let knowledgename = ref("")
let ispublic = ref(true)
let showAddNew = ref(false)
let cid = ref("")
let emit = defineEmits(["addk", "publick","eqa","publishk"])

function publishk(id: string) {
    emit("publishk", id)
}

function addk() {
    emit("addk", knowledgename.value, ispublic.value)
    knowledgename.value = ""
    showAddNew.value = false
}
function eqa(knowledgeid:string) {
    cid.value=knowledgeid
    emit("eqa",knowledgeid)
}

function publick(id: string, k: Knowledge) {
    k.ispublic = !k.ispublic
    emit("publick", id, k)
}
let prop = defineProps({
    "uks": {
        type: Array<Knowledge>,
        default: []
    }
})

</script>
<style scoped>
.kfl,
.ksl {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
}

.kfl>div:first-child,
.ksl>div:first-child {
    width: 100px;
}

.kfl>div:last-child,
.ksl>div:last-child {
    flex: 1
}

.btn {
    display: inline-block;
    border-radius: 3px;
    text-align: center;
    cursor: pointer;
    padding: 3px;
    box-shadow: 0px 0px 3px 3px gainsboro;
    background-color: white;
    user-select: none;
}

.btn:hover {
    background-color: #f0f0f0;
}

.ktl {
    margin-top: 10px;
    display: flex;
    justify-content: space-between;
}

.ktl>div:first-child>div {
    user-select: none;
    display: inline-block;
    background-color: white;
    border:1px solid black;
    text-align: center;
    cursor: pointer;
    padding: 3px;
}
.ktl>div:first-child>div:hover{
    background-color: gainsboro;
}
.publicak {
    background-color: greenyellow !important;
}
.publicak:hover {
    background-color: yellowgreen !important;
}
.k {
        width: 300px;
    margin: 10px;
    padding: 5px;
    border: 1px solid black;
    border-radius: 5px;
    box-shadow: 0px 0px 3px 3px black;
}
.ck{
    background-color:gold;
}
.np{
   color:red;
}
</style>