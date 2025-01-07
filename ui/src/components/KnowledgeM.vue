<template>
    <div class="km">
        <div>
            <div class="content">
                <div>
                    <select class="selectk" v-model="knowledgeid">
                        <option :value="AddStr">Add Knowledge</option>
                        <option v-for="k in prop.uks" :key="k.id" :value="k.id">{{ k.knowledgename }}</option>
                    </select>
                </div>
                <div>
                    <div>
                        Knowledge name:<br>
                        <textarea class="selectk editkname" v-model="showk.knowledgename"></textarea>
                    </div>
                    <div>
                        Share the knowledge:<br>
                        <div class="sharek" @click="showk.ispublic = !showk.ispublic">
                            <div class="yes" :class="{ 'isyesno': showk.ispublic }">Yes</div>
                            <div class="no" :class="{ 'isyesno': !showk.ispublic }">No</div>
                        </div>
                    </div>
                    <div>
                        <div v-if="knowledgeid == AddStr" @click="addk" class="btn">
                            Add
                        </div>
                        <div v-if="isSave" @click="editk(knowledgeid, showk)" class="btn">
                            Save
                        </div>
                    </div>
                </div>

                <div>
                    <ListQA :kqa="prop.kqa" @rmqas="() => { emit('rmqas') }"></ListQA>
                </div>
               
            </div>
        </div>
    </div>
</template>
<script name="klist" setup lang="ts">
import { defineProps, defineEmits, ref, computed, watch } from 'vue'
import ListQA from './ListQA.vue'
import { type Knowledge, type KQA } from '@/types'
let emit = defineEmits(["addk", "publick", "eqa", "publishk", "rmqas"])
let prop = defineProps({
    "uks": {
        type: Array<Knowledge>,
        default: []
    },
    "kqa": {
        type: Object as () => KQA,
        default: () => ({ QAS: [], knowledgeid: "" })
    }
})


let showAddNew = ref(false)
let cid = ref("")
const AddStr = "-Add-"
let knowledgeid = ref(AddStr)
let showk = ref<Knowledge>({
    username: "",
    id: AddStr,
    knowledgename: "",
    ispublic: true,
    currentversion: "",
})
let isSave = computed(() => {
    if (knowledgeid.value == AddStr) {
        return false
    }
    for (let k of prop.uks) {
        if (k.id == knowledgeid.value) {
            return (k.knowledgename != showk.value.knowledgename || k.ispublic != showk.value.ispublic)
        }
    }
    return false
})
watch(knowledgeid, (newv: string) => {
    if (newv == AddStr) {
        showk.value = {
            username: "",
            id: AddStr,
            knowledgename: "",
            ispublic: true,
            currentversion: "",
        }
    }
    for (let k of prop.uks) {
        if (k.id == newv) {
            showk.value = {
                username: k.username,
                id: k.id,
                knowledgename: k.knowledgename,
                ispublic: k.ispublic,
                currentversion: k.currentversion,
            }
        }
    }
    eqa(newv)
})
watch(() =>
    prop.uks
    , () => {
        for (let k of prop.uks) {
            if (k.knowledgename == showk.value.knowledgename && k.ispublic == showk.value.ispublic) {
                knowledgeid.value = k.id
            }
        }
    })
function publishk(id: string) {
    emit("publishk", id)
}
function addk() {
    emit("addk", showk.value.knowledgename, showk.value.ispublic)
    showAddNew.value = false
}
function eqa(knowledgeid: string) {
    if (knowledgeid == AddStr) {
        return
    }
    cid.value = knowledgeid
    emit("eqa", knowledgeid)
}

function editk(id: string, k: Knowledge) {
    if (id == AddStr || k.knowledgename == "") {
        return
    }
    k.ispublic = !k.ispublic
    emit("publick", id, k)
}
</script>
<style lang="css" scoped>
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

.selectk {
    width: 300px;
    font-size: 25px;
    border-radius: 10px;
    padding: 3px;
}

.editkname {
    width: 292px;
    font-size: 25px;
    border-radius: 10px;
    padding: 3px;
    resize: none;
    overflow: hidden;
    white-space: nowrap;
    height: 32px;
}

textarea:focus {
    outline: none;
    border: 1px solid blue;
}

.sharek {
    width: 300px;
    display: flex;
    justify-content: space-between;
    text-align: center;
}

.yes,
.no {
    cursor: pointer;
    border: 1px solid transparent;
    flex: 1;
    background-color: gainsboro;

}

.isyesno {
    background-color: greenyellow;
}
.btn{
    margin-top:5px;
    width: 145px;
    height: 30px;
}
</style>