<template>
    <div style="background-color:#F0F2F6;border-bottom:3px solid #F0F2F6;border-radius: 5px;">
        <div class="qas">
            <div class="qa qah">
                <div v-if="!prop.readonly"><input type="checkbox" v-model="checkall">All
                </div>
                <div style="position: relative;text-align: center;">
                    <div :class="{ 'w100': removelist.length > 0 }">
                        <div v-if="removelist.length > 0 && !prop.readonly" class="rbtn btn" @click="rmqas">Remove</div>
                    </div> question
                </div>
                <div style="text-align: center;">answer</div>
            </div>
        </div>
        <div class="qas yscroll" :style="{ 'height': prop.listh + 'px' }">
            <hr>
            <div v-for="qa, idx in kqa.QAS" :key="qa.id" class="qa qax">
                <div>
                    <input v-if="!prop.readonly" type="checkbox" :checked="removelist.indexOf(qa.id) >= 0"
                        @click.stop="sel(qa.id)">
                    <div v-else>{{ idx + 1 }}</div>
                </div>
                <div>{{ qa.q }}</div>
                <div>{{ qa.a }}</div>
            </div>
        </div>
    </div>

    <div v-show="prop.kqa.knowledgeid != prop.AddStr && !prop.readonly" style="margin-top: 15px;">
        <UploadFile :kid="prop.kqa.knowledgeid" />
    </div>
</template>
<script setup lang="ts">
import { ref, watch, defineProps, defineEmits } from 'vue';
import UploadFile from './UploadFile.vue';
import { type KQA } from '@/types';
const emit = defineEmits(["rmqas", "publish"])
const prop = defineProps({
    "kqa": {
        type: Object as () => KQA,
        default: () => ({ QAS: [], knowledgeid: "" })
    },
    "listh": {
        type: Number,
        default: 100
    },
    "AddStr": {
        type: String,
        default: ""
    },
    readonly: {
        type: Boolean,
        default: true
    }
})
let checkall = ref(false)
let removelist = ref<string[]>([])
async function rmqas() {
    let qas: { id: string }[] = []
    removelist.value.forEach(id => {
        qas.push({ "id": id })
    });
    await emit("rmqas", prop.kqa.knowledgeid, JSON.stringify(qas))
    removelist.value.length = 0
    checkall.value = false
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

</script>
<style scoped>
.qas {
    margin: 5px;
}

.yscroll {
    overflow-y: scroll;
}

.qas>.qa:first-child {
    font-weight: bold;
}

.qax {
    border-bottom: 1px solid #F0F2F6;
    font-size: 13px;
    padding: 1px;
    line-height: 20px;
}

.qax>div:nth-child(2) {
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
    width: 40px;
}

.w100 {
    position: absolute;
    left: 0;
    top: 3px;
}

.qa>div:nth-child(2) {
    flex: 3;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    padding:5px ;
}

.qa>div:nth-child(3) {
    flex: 4;
    word-wrap: break-word;
    word-break: break-all;
    white-space: pre-wrap;
    padding:5px ;
}

.qah>div {
    background-color: #F0F2F6;
}

.rbtn {
    font-size: 13px;
    width: 60px;

}
</style>