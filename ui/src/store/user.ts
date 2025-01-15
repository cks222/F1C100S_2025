import { defineStore } from 'pinia'
import {
    check_user, api_login, api_signup
} from '@/utils/axios'
import { sha256 } from 'js-sha256'

export const useUserStore = defineStore('user', {
    actions: {
        async checkIsLogin() {
            if (localStorage.getItem("userid") != null && localStorage.getItem("token") != null) {
                this.UserId = `${localStorage.getItem("userid")}`
                this.Token = `${localStorage.getItem("token")}`
                const data = await check_user(this.UserId, this.Token)
                this.UserName = data.username
                return <boolean>data.isuser
            }
            this.UserId = ""
            this.Token = ""
            this.UserName = ""
            return false;
        },
        cryptoPass(password: string) {
            let token = sha256(password)
            return token;
        },
        async login(account: string, password: string) {

            const data = await api_login(account, this.cryptoPass(password))
            console.log(data)
            if (data.id != "") {
                this.UserId = data.id
                this.Token = this.cryptoPass(password)
                localStorage.setItem("userid", this.UserId)
                localStorage.setItem("token", this.Token)
                return true
            }
            return false
        },
        logout() {
            this.Token = ""
            this.UserName = ""
            this.UserId = ""
            localStorage.clear()
        },
        async signUp(account: string, password: string, confirmpassword: string) {
            if (password != confirmpassword) {
                throw new Error("两次密码不一致")
            }
            await api_signup(account, this.cryptoPass(password))
        },
        changePassword(username: string, password: string) {

        }
    },
    state() {
        return {
            UserName: "",
            UserId: "",
            Token: "",
        }
    }
})