<template>
    <div v-if="kqa.knowledgeid" @click.stop="uf" class="btn ubtn">Upload File
        <input type="file" ref="preparedfile" :disabled="isuploading" @change="uploadFile" hidden>
    </div>
    <div class="qas">
        <div class="qa">
            <div :class="{ 'w100': removelist.length > 0 }"><input type="checkbox" v-model="checkall">All<div
                    v-if="removelist.length > 0" class="rbtn btn" @click="rmqas">Remove</div>
            </div>
            <div>question</div>
            <div>answer</div>
        </div>
        <hr>
        <div v-for="qa in kqa.QAS" :key="qa.id" class="qa qax">
            <div><input type="checkbox" :checked="removelist.indexOf(qa.id) >= 0" @click.stop="sel(qa.id)"></div>
            <div>{{ qa.q }}</div>
            <div>{{ qa.a }}</div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';

import { useKnowledgeStore } from '@/store/knowledge'
import { type KQA } from '@/types';
const emit = defineEmits(["rmqas"])
const prop = defineProps({
    "kqa": {
        type: Object as () => KQA,
        default: () => ({ QAS: [], knowledgeid: "" })
    }
})
let checkall = ref(false)
const preparedfile = ref<HTMLInputElement>()
let showUpload = ref(false)
let isuploading = ref(false)
let knowledgeStore = useKnowledgeStore()
let removelist = ref<string[]>([])
function rmqas() {
    var data = new FormData();
    let qas: { id: string }[] = []
    removelist.value.forEach(id => {
        qas.push({ "id": id })
    });
    data.append("qas", JSON.stringify(qas))
    console.log(prop.kqa.knowledgeid)
    emit("rmqas", prop.kqa.knowledgeid, data)
}
function sel(id: string) {
    if (removelist.value.indexOf(id) >= 0) {
        removelist.value = removelist.value.filter(x => x != id)
    } else {
        removelist.value.push(id)
    }
}
watch(checkall, (v) => {
    if (v) {
        if (prop.kqa.QAS.length > 0)
            removelist.value = prop.kqa.QAS.map(x => x.id)
    } else {
        removelist.value = []
    }
});

function uf() {
        let hie = <HTMLInputElement>preparedfile.value
        hie.value = ""
        preparedfile.value?.click()
}

async function uploadFile() {
    let files = <FileList>preparedfile.value?.files
    isuploading.value = true
    setTimeout(async () => {
        var formData = new FormData();
        formData.append('file', files[0]);
        await knowledgeStore.upload_file(prop.kqa.knowledgeid, formData)
        let hie = <HTMLInputElement>preparedfile.value
        hie.value = ""
        isuploading.value = false
        knowledgeStore.GetQA(prop.kqa.knowledgeid)
    }, 0)
}
</script>
<style scoped>
.qas {
    margin: 5px;
}

.qas>.qa:first-child {
    font-weight: bold;
}

.qax {
    border-bottom: 1px solid black;
    font-size: 13px;
}

.qax:nth-child(2n) {
    background-color: azure;
}

.qa {
    display: flex;
    justify-content: left;
}

.qa>div:first-child {
    width: 40px;
}

.w100 {
    width: 100px !important;
    ;
}

.qa>div:nth-child(2) {
    flex: 3;
    word-wrap: break-word;
    word-break: break-all;
}

.qa>div:nth-child(3) {
    flex: 4;
    word-wrap: break-word;
    word-break: break-all;
}


.btn {
    display: inline-block;
    border-radius: 3px;
    text-align: center;
    font-weight: initial !important;
    cursor: pointer;
    background-color: white;
    user-select: none;
}
.ubtn{
    margin-top:10px;
    box-shadow: 0px 0px 3px 3px goldenrod;
}
.rbtn{
    font-size: 13px;
    box-shadow: 0px 0px 3px 3px red;
}
.btn:hover {
    background-color: #f0f0f0;
}
</style>