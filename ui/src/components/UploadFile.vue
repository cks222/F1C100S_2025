<template>
    <div @click="selectfile">
        <div class="ufp" @dragover="(e: DragEvent) => { e.preventDefault() }"
            @dragleave="(e: DragEvent) => { e.preventDefault() }" @drop="drop">
            <div :class="{ 'uploading': isuploading }">
                <div>
                    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor"
                        xmlns="http://www.w3.org/2000/svg" color="inherit"
                        class="e14lo1l1 st-emotion-cache-133trn5 ex0cdmw0">
                        <path fill="none" d="M0 0h24v24H0V0z"></path>
                        <path
                            d="M19.35 10.04A7.49 7.49 0 0012 4C9.11 4 6.6 5.64 5.35 8.04A5.994 5.994 0 000 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM19 18H6c-2.21 0-4-1.79-4-4 0-2.05 1.53-3.76 3.56-3.97l1.07-.11.5-.95A5.469 5.469 0 0112 6c2.62 0 4.88 1.86 5.39 4.43l.3 1.5 1.53.11A2.98 2.98 0 0122 15c0 1.65-1.35 3-3 3zM8 13h2.55v3h2.9v-3H16l-4-4z">
                        </path>
                    </svg>
                </div>
            </div>
            <div v-if="!isuploading">

                <div>Drag and drop files here</div>
                <div>Limit 200MB per file</div>
                <div v-if="errormsg != ''" style="color: red;">{{ errormsg }}</div>
            </div>
            <div v-if="isuploading">

                <div>Uploading {{ filename }}</div>

            </div>
            <div>
                <div v-show="!isuploading" class="btn">Browse file</div>
                <input type="file" ref="preparedfile" :disabled="isuploading" @change="uf" hidden accept=".txt" />
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, defineProps, defineEmits } from 'vue';
import { useKnowledgeStore } from '@/store/knowledge';
const knowledgeStore = useKnowledgeStore()
const prop = defineProps({
    kid: {
        type: String,
        default: ""
    }
})

const preparedfile = ref<HTMLInputElement>()
let isuploading = ref(false)
let filename = ref("")
let errormsg = ref("")

function selectfile() {
    let hie = <HTMLInputElement>preparedfile.value
    hie.value = ""
    preparedfile.value?.click()
}

function uploadFile(files: FileList) {
    errormsg.value = ""
    if (files == null || isuploading.value || files.length < 1) {
        return
    }
    filename.value = files[0].name
    if (files[0].size > 200 * 1024 * 1024) {
        errormsg.value = "file size of '" + filename.value + "' is more than 200MB. you can split it to upload."
        return
    }
    isuploading.value = true
    setTimeout(async () => {
        try {
            var formData = new FormData();
            formData.append('file', files[0]);
            await knowledgeStore.upload_file(prop.kid, formData)
            let hie = <HTMLInputElement>preparedfile.value
            hie.value = ""
            isuploading.value = false
            knowledgeStore.GetQA(prop.kid)
        } catch {
            isuploading.value = false
            preparedfile.value = undefined
            errormsg.value = "failed to upload."
        }
    }, 0)
}

function drop(e: DragEvent) {
    e.preventDefault()
    let files = <FileList>e.dataTransfer?.files;
    uploadFile(files)
}

async function uf() {
    let files = <FileList>preparedfile.value?.files
    uploadFile(files)
}
</script>
<style lang="css" scoped>
* {
    user-select: none;
}

.ufp {
    background-color: #F0F2F6;
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-radius: 5px;
    cursor: pointer;
}

.ufp>div:first-child {
    width: 77px;
    color: gray
}

.ufp>div:first-child>div {
    margin-left: 20px;
    width: 37px;
}

.uploading {
    animation: kfuploading 3s infinite;
}

@keyframes kfuploading {

    0%,
    100% {
        color: black
    }

    20%,
    80% {
        color: greenyellow
    }

    50% {
        color: yellow
    }
}

.ufp>div:nth-child(2) {
    flex: 1;
}

.ufp>div:nth-child(2)>div:first-child {
    font-size: 16px;

}

.ufp>div:nth-child(2)>div:last-child {
    font-size: 14px;

}

.ufp>div:last-child {
    width: 100px;
}

.btn {
    width: 90px;
    height: 30px;
    font-size: 16px;
}
</style>