<template>
    <form>
        <div class="container">
            <div class="mb">
                <div style="text-align: center;position: relative;">
                    <label class="icon roll">☯</label>
                </div>
                <div style="height: 230px;"></div>
                <div style="font-size: 32px;text-align: center;font-weight: bold;">
                    {{ mode == constString.MODE_LOGIN ? 'Welcome' : 'Create your account' }}
                </div>
                <br> <br>
                <div>
                    <div v-if="Step == 1">
                        <div class="input-wrapper">
                            <input class="email-input" type="email" v-model="account" id="email-input"
                                @focus="accounthanglabel = true" @focusout="accounthanglabel = false || account != ''"
                                autofocus>
                            <label class="email-label "
                                :class="{ 'hang-label': accounthanglabel, 'cover-label': !accounthanglabel }"
                                for="email-input">Email address</label>
                        </div>
                    </div>
                    <div v-if="Step == 2">
                        <div class="input-wrapper">
                            <input class="email-input" type="email" :value="account" readonly>
                            <div class="input-setting" @click="Step = 1">Edit</div>
                        </div>
                        <div class="input-wrapper">
                            <input class="pwd-input" :type="showpwd ? 'text' : 'password'" v-model="pwd" id="pwd-input"
                                @focus="pwdhanglabel = true" @focusout="pwdhanglabel = false || pwd != ''" autofocus>
                            <label class="pwd-label"
                                :class="{ 'hang-label': pwdhanglabel, 'cover-label': !pwdhanglabel }"
                                for="pwd-input">Password</label>
                            <div class="input-setting" @click="showpwd = !showpwd">
                                <div v-if="showpwd" v-html="SvgShowEye"></div>
                                <div v-if="!showpwd" v-html="SvgHideEye"></div>

                            </div>
                        </div>
                    </div>
                    <div v-if="mode == constString.MODE_SIGNUP && Step == 2">
                        <div class="input-wrapper">
                            <input class="pwd-input" :type="showcfmpwd ? 'text' : 'password'" v-model="cfmpwd"
                                id="pwd-input" @focus="cfmpwdhanglabel = true"
                                @focusout="cfmpwdhanglabel = false || cfmpwd != ''" autofocus>
                            <label class="pwd-label"
                                :class="{ 'hang-label': cfmpwdhanglabel, 'cover-label': !cfmpwdhanglabel }"
                                for="pwd-input">Password</label>
                            <div class="input-setting" @click="showcfmpwd = !showcfmpwd">
                                <div v-if="showcfmpwd" v-html="SvgShowEye"></div>
                                <div v-if="!showcfmpwd" v-html="SvgHideEye"></div>
                            </div>
                        </div>
                    </div>
                    <div class="msg" v-show="errmsg != ''">{{ errmsg }}</div>
                    <div class="bt">
                        <div>
                            <div class="btn" @click="NextStep">Continue</div>
                        </div>
                        <br>
                        <div style="text-align: center;">
                            <div v-show="mode != constString.MODE_SIGNUP">
                                Don't have an account? <div class="changemode"
                                    @click="Step = 1; mode = constString.MODE_SIGNUP">Sign Up</div>
                            </div>
                            <div v-show="mode != constString.MODE_LOGIN">
                                Already have an account? <div class="changemode"
                                    @click="Step = 1; mode = constString.MODE_LOGIN">Login</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </form>
</template>
<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from "@/store/user";

const router = useRouter()
const userStore = useUserStore()
let constString = {
    MODE_SIGNUP: "Sign up",
    MODE_LOGIN: "Login",
}
let Step = ref(1);

const SvgShowEye = "<svg width='18' height='15' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'><defs><path d='M12.148 5.969a3.5 3.5 0 0 1-4.68 4.68l.768-.768a2.5 2.5 0 0 0 3.145-3.145l.767-.767zM5.82 12.297c.993.47 2.052.703 3.18.703 3.13 0 5.732-1.788 7.856-5.5-.837-1.463-1.749-2.628-2.738-3.501l.708-.708C15.994 4.337 17.052 5.74 18 7.5c-2.333 4.333-5.333 6.5-9 6.5a8.294 8.294 0 0 1-3.926-.957l.746-.746zM15.89.813L2.313 14.39a.5.5 0 0 1-.667-.744L3.393 11.9C2.138 10.837 1.007 9.37 0 7.5 2.333 3.167 5.333 1 9 1c1.51 0 2.907.367 4.19 1.102L15.147.146a.5.5 0 0 1 .744.667zm-3.436 2.026A7.315 7.315 0 0 0 9 2C5.87 2 3.268 3.788 1.144 7.5c.9 1.572 1.884 2.798 2.959 3.69l1.893-1.893a3.5 3.5 0 0 1 4.801-4.801l1.657-1.657zm-2.396 2.395a2.5 2.5 0 0 0-3.324 3.324l3.324-3.324z' id='a' /></defs><g fill='none' fill-rule='evenodd'><mask id='b' fill='#fff'><use xlink:href='#a' /></mask><use fill='#5C677D' fill-rule='nonzero' xlink:href='#a' /><g mask='url(#b)' fill='#5C677D'><path d='M-1-3h20v20H-1z' /></g></g></svg>"
const SvgHideEye = "<svg width='18' height='13' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'><defs><path d='M9 12c3.13 0 5.732-1.788 7.856-5.5C14.732 2.788 12.13 1 9 1S3.268 2.788 1.144 6.5C3.268 10.212 5.87 12 9 12zM9 0c3.667 0 6.667 2.167 9 6.5-2.333 4.333-5.333 6.5-9 6.5s-6.667-2.167-9-6.5C2.333 2.167 5.333 0 9 0zm0 9a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zm0 1a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7z' id='a' /></defs><g fill='none' fill-rule='evenodd'><mask id='b' fill='#fff'><use xlink:href='#a' /></mask><use fill='#5C677D' fill-rule='nonzero' xlink:href='#a' /><g mask='url(#b)' fill='#5C677D'><path d='M-1-4h20v20H-1z' /></g></g></svg>"

let mode = ref(constString.MODE_LOGIN)
let account = ref("")
let pwd = ref("")
let cfmpwd = ref("")
let errmsg = ref("")
let showpwd = ref(false)
let showcfmpwd = ref(false)
let accounthanglabel = ref(false)
let pwdhanglabel = ref(false)
let cfmpwdhanglabel = ref(false)

watch(() => {
    return account.value + pwd.value + cfmpwd.value
}, () => {
    errmsg.value = ""
})

async function NextStep() {
    if (Step.value == 1) {
        if (account.value.trim() == "") {
            errmsg.value = "please enter a account."
            return
        }
        Step.value++
    } else if (constString.MODE_LOGIN == mode.value) {
        await login()
    } else if (constString.MODE_LOGIN == mode.value) {
        await signup()
    }
}

async function signup() {
    await userStore.signUp(account.value, pwd.value, cfmpwd.value)
    await login()
}
async function login() {
    if (!await userStore.login(account.value, pwd.value)) {
        errmsg.value = "account and password do not match"
    } else {
        router.replace({ name: "knowledge" })
    }
}
</script>
<style scoped>
.container {
    display: flex;
    justify-content: center;
    /*background: linear-gradient(white, lightgray, black);*/
    min-height: 100vh;
}

.mb {
    margin-top: 100px;
    width: 340px;
    min-height: 400px;
}


.input-wrapper {
    position: relative;
    margin-bottom: 25px;
    box-sizing: content-box;
}

.email-input,
.pwd-input {
    appearance: none;
    background-color: #fff;
    border: 1px solid #c2c8d0;
    border-radius: 6px;
    box-sizing: border-box;
    color: #2d333a;
    font-family: inherit;
    font-size: 16px;
    height: 52px;
    line-height: 1.1;
    outline: none;
    padding-block: 1px;
    padding-inline: 2px;
    padding: 0 16px;
    transition: box-shadow .2s ease-in-out, border-color .2s ease-in-out;
    width: 100%;
    text-rendering: auto;
    letter-spacing: normal;
    word-spacing: normal;
    text-transform: none;
    text-indent: 0;
    text-shadow: none;
    display: inline-block;
    text-align: start;
    margin: 0;
}

.email-label,
.pwd-label {
    font-size: 12px;
    left: 10px;
    top: 0px;
    position: absolute;
    background-color: #fff;
    color: #6f7780;
    font-weight: 400;
    margin-bottom: 8px;
    max-width: 90%;
    overflow: hidden;
    pointer-events: none;
    padding: 1px 6px;
    text-overflow: ellipsis;
    transform: translateY(-50%);
    transform-origin: 0;
    transition: transform .15s ease-in-out, top .15s ease-in-out, padding .15s ease-in-out;
    white-space: nowrap;
    z-index: 1;
}

.input-setting {
    position: absolute;
    right: 16px;
    font-size: 16px;
    top: 16px;
}

.hang-label {
    animation: moveTop 0.3s forwards;
}

.cover-label {
    animation: moveCover 0.3s forwards;
}


@keyframes moveTop {
    from {
        font-size: 16px;
        left: 16px;
        top: 26px;
    }

    to {
        font-size: 12px;
        left: 10px;
        top: -7px;
    }
}

@keyframes moveCover {
    from {
        font-size: 12px;
        left: 10px;
        top: -7px;
    }

    to {
        font-size: 16px;
        left: 16px;
        top: 26px;
    }
}

input[type="password"]::-ms-reveal,
input[type="password"]::-ms-clear {
    display: none;
}

.btn {
    background-color: #10a37f;
    color: #ffffff;
    padding-top: 10px;
    padding-bottom: 10px;
}

.icon {
    left: 130px;
    display: inline-block;
    font-size: 80px;
    height: 80px;
    width: 80px;
    line-height: 80px;
    padding: 0;
    margin-top: 0;
    position: absolute;
}

.roll {
    animation: roll-animation 3s infinite linear;
}

@keyframes roll-animation {
    0% {
        color: black;
    }

    50% {
        color: gray
    }

    100% {
        transform: rotate(360deg);
        color: black;
    }
}

.changemode {
    display: inline-block;
    color: #10a37f;
    cursor: pointer;
}

.msg {
    color: red;
    font-size: 12px;
}
</style>
