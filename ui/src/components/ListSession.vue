<template>
    Please select a session or create a new session.
    <hr>
    <div v-for="ss in ssssx" :class="{ 'os': true, 'active': ss.SessionId == prop.sid }">
        <div @click="switchsession(ss.SessionId)" class="sl">
            <div>Knowledge:{{ ss.KnowledgeName }}
                <div>{{ ss.QTime }}~{{ ss.ATime }}</div>
            </div>
            <div v-if="ss.Q != ''">
                <div></div>
                <div>{{ ss.Q }}</div>:<div>User</div>
            </div>
            <div v-if='ss.A != ""'>
                <div>AI</div>:<div>{{ ss.A }}</div>
                <div></div>
            </div>
        </div>
    </div>
    <div class="os">
        <div class="sl">
            <div>Knowledge:
                <select v-model="kid">
                    <option v-for="k in ks" :value="k.id">{{ k.knowledgename }}</option>
                </select>
            </div>
        </div>

        <div class="addnew">
            <div></div>
            <div class="btn" @click="newsss">Create Session</div>
        </div>
    </div>
</template>
<script setup lang="ts">
import { defineProps, defineEmits, ref, computed } from 'vue';
import { type Session, type Knowledge, type SessionHistory, type SessionDisplay } from '@/types';
const emit = defineEmits(["ss", "as", "tc"])
let ks = computed(() => {
    return prop.ks.filter(x => x.currentversion != "")
})
let ssssx = computed<SessionDisplay[]>(() => {
    let result = []
    for (let ss of prop.sss) {
        let kn = getkname(ss.knowledgeid)
        let Q = "", A = "", QTime = "Not Start", ATime = "Now"
        prop.shl.forEach(s => {
            if (s.SessionId == ss.sessionid) {
                if (s.Messages.length >= 1) {
                    Q = s.Messages[0].Content
                    QTime = s.Messages[0].Time
                }
                if (s.Messages.length >= 2) {
                    A = s.Messages[s.Messages.length - 1].Content
                    ATime = s.Messages[s.Messages.length - 1].Time
                }
            }
        })
        result.push({ SessionId: ss.sessionid, KnowledgeName: kn, Q: Q, A: A, QTime: QTime, ATime: ATime })

    }
    result.sort((a, b) => new Date(b.ATime).getTime() - new Date(a.ATime).getTime())
    return result
})
const prop = defineProps({
    "sss": {
        type: Array<Session>,
        default: []
    },
    "ks": {
        type: Array<Knowledge>,
        default: []
    },
    "shl": {
        type: Array<SessionHistory>,
        default: []
    },
    "sid": {
        type: String,
        default: ""
    }
})
let kid = ref("")
function getkname(id: string) {
    for (let k of prop.ks) {
        if (k.id == id) {
            return k.knowledgename
        }
    }
    return "not found"
}
function switchsession(id: string) {
    emit('ss', id)
    emit("tc")
}
function newsss() {
    if (kid.value == "") {
        console.log("no knowledge selected")
        return
    }
    emit("as", kid.value)
    emit("tc")
}
</script>
<style scoped>
.os {
    width: 350px;
    border: 1px solid black;
    margin-top: 3px;
}

.sl {
    cursor: pointer;
    padding: 3px;
}

.sl>div:first-child {
    text-align: center;
}

.sl>div:nth-child(2)>div:last-child,
.sl>div:nth-child(3)>div:first-child,
.sl>div:nth-child(2)>div:first-child,
.sl>div:nth-child(3)>div:last-child {
    display: inline-block;
    width: 40px;
    border-radius: 10px;
    text-align: center;
}

.sl>div:nth-child(2)>div:last-child,
.sl>div:nth-child(3)>div:first-child {
    border: 1px solid black;

}

.sl>div:nth-child(2)>div:nth-child(2),
.sl>div:nth-child(3)>div:nth-child(2) {
    flex: 1;
    display: inline-block;
    max-width: 200ch;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.sl>div:nth-child(2) {
    display: flex;
    align-items: start;
    text-align: right;
}

.sl>div:nth-child(3) {
    display: flex;
    align-items: start;
    text-align: left;
}

.addnew {
    display: flex;
    padding: 3px;
    margin-top: 10px;
}

.addnew>div:first-child {
    flex: 1;
}


.btn {
    background-color: antiquewhite;
    border-radius: 5px;
    padding: 3px;
    cursor: pointer;
    text-align: center;
}

.btn:hover {
    background-color: lightcyan;
}

.active {
    background-color: gold;
    box-shadow: 0 0 5px 5px gold;
}
</style>