<template>
    <Navigator></Navigator>
    <div style="display: flex;">
        <div style="width: 350px;">
            <ListKnowledge :uks="UserKnowledges" @addk="knowledgeStore.AddKnowledge"
                @publick="knowledgeStore.updateKnowledge" @eqa="eqa"
                @publishk="knowledgeStore.PublishKnowledge"></ListKnowledge>
        </div>
        <div style="flex:1">
            <ListQA :kqa="QA" @rmqas="knowledgeStore.RemoveQA"></ListQA>
        </div>
    </div>
</template>
<script name="management" setup lang="ts">
import ListKnowledge from '@/components/ListKnowledge.vue'
import ListQA from '@/components/ListQA.vue'
import Navigator from '@/components/Navigator.vue'
import { useKnowledgeStore } from '@/store/knowledge'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

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