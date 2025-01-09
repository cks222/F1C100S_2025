import { createRouter, createWebHistory } from 'vue-router'
import ChatPage from "@/pages/ChatPage.vue"
import KnowledgeM from "@/pages/KnowledgeM.vue"
import Login from "@/pages/Login.vue"
import Layout from '@/pages/Layout.vue'
import { check_user } from "@/utils/axios"
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            name: "login",
            path: "/login",
            component: Login,
            meta: {
                title: "登录"
            }
        },
        {
            name: "layout",
            path: "/layout",
            component: Layout,
            children: [
                {
                    name: "chat",
                    path: "/chat",
                    component: ChatPage,
                    meta: {
                        title: "询问"
                    }
                },
                {
                    name: "knowledge",
                    path: "/knowledge",
                    component: KnowledgeM,
                    meta: {
                        title: "知识"
                    }
                }
            ]
        },
        {
            path: '/',
            redirect: "/login"
        }
    ]
})
async function checklogin() {

    if (localStorage.getItem("userid") != null && localStorage.getItem("token") != null) {
        let userid = `${localStorage.getItem("userid")}`
        let token = `${localStorage.getItem("token")}`
        const response = await check_user(userid, token)
        let result = <boolean>response.data.isuser
        if (!result) {
            localStorage.clear()
        }
        return result
    }
    return false;
}
router.beforeEach(async (to, from, next) => {
    if (to.name != "login") {
        if (await checklogin()) {
            if (to.name == "layout") {
                next({ name: "knowledge" })
            } else {
                next()
            }
            return
        }
        next("/login")
    } else {
        if (localStorage.getItem("userid") != null && localStorage.getItem("token") != null) {
            if (from != undefined)
                next("/knowledge")
        }
        next()
    }
})
router.afterEach((to, from) => {
    document.title = <string>to.meta.title
})
export default router