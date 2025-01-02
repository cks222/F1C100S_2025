<template>
    <form>
        <div class="container">
            <div class="mb">
                <div class="ttl">
                    {{ mode }}
                </div>
                <div class="ap">
                    <div>
                        <div>账</div>
                        <div>号:</div>
                    </div>
                    <div><input type="text" v-model="account"></div>
                </div>
                <div class="ap">
                    <div>
                        <div>密</div>
                        <div>码:</div>
                    </div>
                    <div><input type="password" v-model="pwd"></div>
                </div>
                <div class="ap" v-show="isShowConfirmPwd">
                    <div>
                        <div>确</div>
                        <div>认</div>
                        <div>密</div>
                        <div>码:</div>
                    </div>
                    <div><input type="password" v-model="cfmpwd"></div>
                </div>
                <div class="msg" v-show="errmsg != ''">{{ errmsg }}</div>
                <div class="bt">
                    <div>
                        <input type="button" @click="signup" v-show="mode == constString.MODE_SIGNUP"
                            :value="constString.MODE_SIGNUP" />
                        <input type="button" @click="login" v-show="mode == constString.MODE_LOGIN"
                            :value="constString.MODE_LOGIN" />
                    </div>
                    <div>
                        <div @click="mode = constString.MODE_SIGNUP" v-show="mode != constString.MODE_SIGNUP">去注册</div>
                        <div @click="mode = constString.MODE_LOGIN" v-show="mode != constString.MODE_LOGIN">去登陆</div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>
<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from "@/store/user";

const router = useRouter()
const userStore = useUserStore()
let constString = {
    MODE_SIGNUP: "注 册",
    MODE_LOGIN: "登 陆"
}

let mode = ref(constString.MODE_LOGIN)
let account = ref("")
let pwd = ref("")
let cfmpwd = ref("")
let errmsg = ref("")

async function signup() {
   await userStore.signUp(account.value, pwd.value, cfmpwd.value)
    await login()
}
async function login() {
    if (!await userStore.login(account.value, pwd.value)) {
        errmsg.value = "账户或密码错误"
    } else {
        router.replace({ name: "chat" })
    }
}
let isShowConfirmPwd = computed(() => {
    return mode.value == constString.MODE_SIGNUP
})
</script>
<style scoped>
.container {
    display: flex;
    justify-content: center;
    background: linear-gradient(white, lightgray, black);
    min-height: 100vh;
}

.mb {
    margin-top: 100px;
    width: 300px;
    min-height: 400px;
}

.ap {
    width: 260px;
    display: flex;
    justify-content: space-between;
    padding-bottom: 20px;
}

.ap>div:first-child {
    display: flex;
    justify-content: space-between;
    width: 70px;
}

.ap>div>div:last-child {
    text-align: right;
}

.ap>div:last-child {
    flex: 1;
    text-align: right;
}

.ap>div:last-child>input {
    width: 170px;
}

.bt {
    width: 260px;
    display: flex;
    justify-content: space-around;
}

.bt>div {
    flex: 1;
    text-align: right;
}

.bt>div:first-child>input {
    width: 100px
}

.bt>div:last-child>div {
    display: inline-block;
    color: blue;
    text-decoration: underline;
    cursor: pointer;
}

.ttl {
    text-align: center;
    font-size: 40px;
    padding-bottom: 50px;
}

.msg {
    color: red;
}
</style>
