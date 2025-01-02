import { createRouter, createWebHistory } from 'vue-router'
import Chat from "@/pages/Chat.vue"
import Management from "@/pages/Management.vue"
import Login from "@/pages/Login.vue"

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
            name: "chat",
            path: "/chat",
            component: Chat,
            meta: {
                title: "询问"
            }
        },
        {
            name: "management",
            path: "/management",
            component: Management,
            meta: {
                title: "管理"
            }           
        },
        {
            path: '/',
            redirect: "/login"
        }
    ]
})

router.beforeEach(async (to, from, next) => {
    window.speechSynthesis.cancel();
    if (to.name != "login" && to.name != "loginUc") {
        if (localStorage.getItem("userName") != null && localStorage.getItem("token") != null) {
            if (to.name == "main") {
                next({ name: "chat" })
            } else {
                next()
            }
            return
        }
        next("/login")
    } else {
        if (localStorage.getItem("userName") != null && localStorage.getItem("token") != null) {
            if (from != undefined)
                next("/chat")
        }
        next()
    }
})
router.afterEach((to, from) => {
    document.title = <string>to.meta.title
})
export default router