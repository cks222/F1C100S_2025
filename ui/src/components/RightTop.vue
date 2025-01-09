<template>
    <div class="rt">
        <div class="showusetting">
            <div>{{ userStore.UserName }}</div>
            <div class="usetting">
                <div style="position: relative;">
                    <div class="btn">Change password</div>
                    <div class="btn" @click="logout">logout</div>
                </div>
            </div>
        </div>
        <div></div>
    </div>
</template>
<script lang="ts" setup>

import { onMounted } from 'vue'
import { useUserStore } from "@/store/user";
import { useRouter } from 'vue-router'
const userStore = useUserStore()
onMounted(() => {
    userStore.checkIsLogin()
})


const r = useRouter()
function logout() {
    userStore.logout()
    r.push({ name: "login" })
}
</script>
<style lang="css" scoped>
.rt {
    display: flex;
    padding-top: 10px;
    justify-content: right;
}

.rt>div:last-child {
    width: 40px;
}

.showusetting {
    border-radius: 5px;
    cursor: pointer;
    text-align: center;
    width: 150px;
    height: 20px;
    position: relative;
}

.showusetting:hover {
    background-color: azure;
}

.usetting {
    display: none;
    width: 140px;
    right: 0;
    top: 20px;
    position: absolute;
    border-radius: 5px;
    padding: 0 5px 5px 5px;
    background-color: gainsboro;
    opacity: 0.8;
}

.showusetting:hover>.usetting {
    display: block !important;
}

.usetting>div>div:hover {
    background-color: white;
}

.btn {
    margin-top: 5px;
}
</style>