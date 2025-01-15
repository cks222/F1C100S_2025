<template>
    <div class="km">
        <div>
            <div class="content">
                <div style="font-size: 30px;font-weight: bold;">
                    📚 Knowledge
                </div>
                <div v-show="!showEdit">
                    <div style="display: flex;">
                        <select class="selectk" v-model="knowledgeid">
                            <option v-for="k in UserKnowledges" :key="k.id" :value="k.id">{{ k.knowledgename }}</option>
                        </select>
                        <div v-show="notreadonly.value" style="font-size: 30px;cursor: pointer;" title="edit"
                            @click="clickeditoradd('edit')">
                            ⚒️</div>
                        <div style="font-size: 30px;cursor: pointer;" title="add new" @click="clickeditoradd('add')">➕
                        </div>

                        <div v-show="!notreadonly.value" style="user-select: none;margin-left: 50px;" title="Owner">
                            <div style="height: 15px;"></div>
                            <div>
                                <label style="font-size: 12px;">created by </label>
                                <label style="font-size: 16px;font-weight: bold;"> {{ notreadonly.owner }} </label>
                                <label style="font-size: 12px;"> at {{ notreadonly.version }}</label>
                            </div>
                        </div>
                    </div>
                </div>
                <div v-show="showEdit" class="editp">
                    <div>{{ knowledgeid == AddStr ? "Create new Knowledge" : ("Edit the Knowledge, name : " + oldname)
                        }}</div>
                    <div>
                        <textarea ref="kn" class="selectk editkname" v-model="showk.knowledgename"
                            placeholder="input knowledge name here"></textarea>
                    </div>
                    <div>
                        Share the knowledge?<br>
                        <div class="sharek" @click="showk.ispublic = !showk.ispublic">
                            <div class="yes" :class="{ 'isyesno': showk.ispublic }">Yes</div>
                            <div class="no" :class="{ 'isyesno': !showk.ispublic }">No</div>
                        </div>
                    </div>
                    <div style="display: flex; justify-content: space-between; width: 300px;">
                        <div v-if="knowledgeid == AddStr && showk.knowledgename != ''" @click="addk" class="btn">
                            Add
                        </div>
                        <div v-if="isSave" @click="editk(knowledgeid, showk)" class="btn">
                            Save
                        </div>
                        <div v-if="showcancel" @click="showEdit = false; knowledgeid = tmpid;" class="btn">
                            Cancel
                        </div>
                    </div>
                </div>

                <div v-show="!showEdit">
                    <ListQA :kqa="kqa" :AddStr="AddStr" :listh="listh" :readonly="!notreadonly.value"
                        @rmqas="async (knowledgeid: string, qas: string) => await knowledgeStore.RemoveQA(knowledgeid, qas)">
                    </ListQA>
                </div>
                <div v-show="showpublish && notreadonly.value" class="btn publish"
                    @click="() => { knowledgeStore.PublishKnowledge(knowledgeid) }">
                    Publish
                </div>
            </div>
        </div>
    </div>
</template>
<script name="klist" setup lang="ts">
import ListQA from '@/components/ListQA.vue'
import { onMounted, ref, computed, watch, nextTick } from 'vue'
import { storeToRefs } from 'pinia'
import { type Knowledge, type KQA } from '@/types'
import { useKnowledgeStore } from '@/store/knowledge'

const AddStr = "-Add-"
const AUTO_PUBLISH=true
let knowledgeStore = useKnowledgeStore()
let { UserKnowledges, QA, UserId } = storeToRefs(knowledgeStore)
let kn = ref()
let showEdit = ref(false)
let knowledgeid = ref(AddStr)
let tmpid = ref(AddStr)
let showk = ref<Knowledge>({
    userid: "",
    username: "",
    id: AddStr,
    knowledgename: "",
    haschange: true,
    ispublic: true,
    currentversion: "",
})
let oldname = computed<string>(() => {
    for (let k of UserKnowledges.value) {
        if (k.id == knowledgeid.value) {
            return k.knowledgename
        }
    }
    return ""
})
let showcancel = computed(() => {
    if (UserKnowledges.value.length == 0 && AddStr == knowledgeid.value) {
        return false
    }
    return true
})
let showpublish = computed(() => {
    if (AUTO_PUBLISH){
        return false
    }
    if (showEdit.value) {
        return false;
    }
    if (knowledgeid.value == AddStr) {
        return false;
    }
    for (let k of UserKnowledges.value) {
        if (knowledgeid.value == k.id) {
            return k.haschange
        }
    }
    return false;
})
let kqa = computed<KQA>(() => {
    if (knowledgeid.value == QA.value.knowledgeid) {

        return QA.value
    } else {
        return { knowledgeid: knowledgeid.value, QAS: [] }
    }
})
let notreadonly = computed(() => {
    let result = false
    let owner = ""
    let at = ""
    for (let k of UserKnowledges.value) {
        if (k.id == knowledgeid.value && knowledgeid.value != AddStr) {
            result = k.userid == UserId.value
            owner = k.username
            at = k.currentversion.split('.')[0] 
        }
    }
    return { "value": result, "owner": owner, "version": at}
})
let isSave = computed(() => {
    if (knowledgeid.value == AddStr) {
        return false
    }
    for (let k of UserKnowledges.value) {
        if (k.id == knowledgeid.value) {
            return (k.knowledgename != showk.value.knowledgename || k.ispublic != showk.value.ispublic)
        }
    }
    return false
})
watch(knowledgeid, (newv: string) => {
    if (newv == AddStr) {
        showk.value = {
            userid: "",
            username: "",
            id: AddStr,
            knowledgename: "",
            haschange: true,
            ispublic: true,
            currentversion: "",
        }
        return
    }
    for (let k of UserKnowledges.value) {
        if (k.id == newv) {
            showk.value = {
                userid: k.userid,
                username: "",
                id: k.id,
                haschange: k.haschange,
                knowledgename: k.knowledgename,
                ispublic: k.ispublic,
                currentversion: k.currentversion,
            }
        }
    }
    setTimeout(() => { eqa(newv) }, 0)

})
function clickeditoradd(method: string) {
    showEdit.value = true;
    if (method == "add") {
        tmpid.value = knowledgeid.value;
        knowledgeid.value = AddStr;
    }
    nextTick(() => { kn.value.focus(); });
}
async function addk() {
    knowledgeid.value = await knowledgeStore.AddKnowledge(showk.value.knowledgename, showk.value.ispublic)
    showEdit.value = false
}
async function eqa(knowledgeid: string) {
    if (knowledgeid == AddStr) {
        return
    }
    await knowledgeStore.GetQA(knowledgeid)
}

async function editk(id: string, k: Knowledge) {
    if (id == AddStr || k.knowledgename == "") {
        return
    }
    k.ispublic = !k.ispublic
    await knowledgeStore.updateKnowledge(id, k)
    showEdit.value = false
}
onMounted(async () => {
    await knowledgeStore.init()
    if (UserKnowledges.value.length > 0) {
        knowledgeid.value = UserKnowledges.value[0].id
        tmpid.value = knowledgeid.value
        setTimeout(() => { eqa(knowledgeid.value) }, 0)
    } else {
        showEdit.value = true
    }

})
let listh = computed(() => {
    let height = document.documentElement.scrollHeight;
    let result = height - 370;
    return result <= 100 ? 100 : result;
})
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


.editkname {
    width: 291px;
    font-size: 25px;
    border-radius: 10px;
    padding: 4px 0px 2px 7px;
    resize: none;
    overflow: hidden;
    white-space: nowrap;
    height: 34px;
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
    background-color: #F0F2F6;

}

.isyesno {
    background-color: greenyellow;
}

.btn {
    margin-top: 5px;
    width: 145px;
    height: 30px;
}

.editp>div {
    margin-top: 15px;
}

.publish {
    margin-top: 10px !important;
    box-shadow: 0px 0px 2px 2px red;
}
</style>