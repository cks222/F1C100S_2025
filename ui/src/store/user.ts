import { defineStore } from 'pinia'
import { get, post } from '@/utils/axios'
import config from '@/config'
import { sha256 } from 'js-sha256'

export const useUserStore = defineStore('user', {
    actions: {
        async checkIsLogin() {
            if (localStorage.getItem("userName") != null && localStorage.getItem("token") != null) {
                this.userName = `${localStorage.getItem("userName")}`
                this.token = `${localStorage.getItem("token")}`
                return true;
            }
            this.userName = ""
            this.token = ""
            return false;
        },
        cryptoPass(password: string) {
            let token = sha256(password)
            return token;
        },
        async login(userName: string, password: string) {
            var formData = new FormData();
            formData.append("username", userName);
            formData.append("token", this.cryptoPass(password));
            const result = await post(config.api.post.login, formData)
            console.log(result.data)
            if (result.data == userName) {
                this.userName = userName
                this.token = this.cryptoPass(password)
                localStorage.setItem("userName", this.userName)
                localStorage.setItem("token", this.token)
                return true
            }
            return false
        },
        logout() {
            this.userName = ""
            this.token = ""
            localStorage.clear()
        },
        async signUp(username: string, password: string, confirmpassword: string) {
            if (password != confirmpassword) {
                throw new Error("两次密码不一致")
            }
            var formData = new FormData();
            formData.append("username", username);
            formData.append("token", this.cryptoPass(password));
            await post(config.api.post.signup, formData)
        },
        changePassword(username: string, password: string) {

        }
    },
    state() {
        return {
            userName: "",
            token: "",
        }
    }
})