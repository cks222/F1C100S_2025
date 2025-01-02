<template>
    <div style="border:1px solid black;padding: 10px;margin-top: 10px;">
        <div >
            <input type="file" ref="preparedfile" :disabled="isuploading">
            <div @click="uploadFile">upload</div>
        </div>
        <div>{{ msg }}</div>
    </div>
</template>
<script setup lang="ts">
import { ref } from 'vue';

import { useKnowledgeStore } from '@/store/knowledge'
import { defineProps } from 'vue';
const prop = defineProps({
  "knowledgeid": {
    type: String,
    default: ""
  }
})

const preparedfile = ref<HTMLInputElement>()
let msg = ref("")
let isuploading = ref(false)
let knowledgeStore = useKnowledgeStore()
let knowledgename = ref("")

async function uploadFile() {
    let files = <FileList>preparedfile.value?.files
    if (files.length == 0) {
        msg.value = "please select a file."
        return
    } else if (isuploading.value) {
        msg.value = "now uploading, please wait."
        return
    }
    msg.value = "uploading..."
    isuploading.value = true
    setTimeout(async () => {
        var formData = new FormData();
        formData.append('file', files[0]);
        await knowledgeStore.upload_file(prop.knowledgeid,formData)
        msg.value = "uploaded " + files[0].name
        let hie = <HTMLInputElement>preparedfile.value
        hie.value = ""
        isuploading.value = false
    }, 3000)
}
</script>
<style scoped>
.ufo {
    display: flex;
    justify-content: left;
}

.ufo>input {
    width: 160px;
}

.ufo>div {
    border-radius: 3px;
    text-align: center;
    width: 70px;
    box-shadow: 0px 0px 2px 2px black;
    cursor: pointer;
}

.ufoa>div {
    background-color: white;
}

.ufod>div {
    background-color: gainsboro;
}

.ufoa>div:hover {
    box-shadow: 0px 0px 2px 2px green;
    background-color: antiquewhite;
}
</style>