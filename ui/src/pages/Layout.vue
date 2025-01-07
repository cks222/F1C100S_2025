<template>
    <div class="topc"></div>
    <div style="display: flex;justify-content: space-between;">
        <div v-show="isHidden" class="showsb" @click="isHidden = false ">
            <div></div>
        </div>
        <div class="leftbar" :class="{ 'is-hidden': isHidden,'not-hidden': !isHidden, }">
            
            <LeftBar @h="() => { isHidden = true }"></LeftBar>
        </div>
        <div style="flex:1;">
            <RightTop></RightTop>

            <KnowledgeM :uks="UserKnowledges" 
              :kqa="QA"
            @addk="knowledgeStore.AddKnowledge"
                @publick="knowledgeStore.updateKnowledge" @eqa="eqa"
                @publishk="knowledgeStore.PublishKnowledge"
               @rmqas="knowledgeStore.RemoveQA"
                ></KnowledgeM>
        </div>
    </div>
</template>
<script setup lang="ts">
import LeftBar from '@/components/LeftBar.vue'
import RightTop from '@/components/RightTop.vue'
import KnowledgeM from '@/components/KnowledgeM.vue'
import { useKnowledgeStore } from '@/store/knowledge'
import { storeToRefs } from 'pinia'
import { ref , onMounted} from 'vue';
let isHidden = ref(false)

let knowledgeStore = useKnowledgeStore()
let { UserKnowledges, QA } = storeToRefs(knowledgeStore)
onMounted(() => {
    knowledgeStore.init()
})
function eqa(knowledgeid: string) {
    knowledgeStore.GetQA(knowledgeid)
    console.log(QA)
}

</script>
<style scoped>
.topc{
    z-index: 1000;
    position: fixed;
    height: 3px;
    width: 100vw;
    top:0px;
    background: linear-gradient(to right, red,yellow,green)
}
.leftbar {
    width: 350px;
}


@keyframes hidelb {
    0%  { width: 350px; }
    30% {display: none;}
    80% { transform: translateX(-100%); }
    100% { width: 0;display: none;}
}

@keyframes showlb {
    0% { width: 350px;display: block;transform: translateX(-100%); }
    100% { width: 350px;display: block; transform: translateX(0%); }
}
.leftbar.not-hidden {
    width: 100%;
    animation: showlb 0.10s forwards;
}
.leftbar.is-hidden {
    width: 100%;
    animation: hidelb 0.20s forwards;
}

.showsb {
    position: absolute;
    left: 20px;
    top: 20px;
    cursor: pointer;
    background-color: transparent;
    border-radius: 10px;
}

.showsb>div::before {
    content: '';
    display: inline-block;
    height: 0px;
    width: 0px;
    border-top: 10px solid transparent;
    border-left: 14px solid rgb(49, 47, 47);
    border-bottom: 10px solid transparent;
    margin: 6px 6px 3px 6px;
}

.showsb:hover>div::before {
    border-left: 14px solid black;
}
</style>