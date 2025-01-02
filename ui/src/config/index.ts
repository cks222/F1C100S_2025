export default {
    host: "http://localhost:1234",
    textMaxLengthMobile: 220,
    textMaxLengthPC: 300,
    headers: {
        headers: {
            "Access-Control-Allow-Origin": "*"
        }
    },
    api: {
        get: {
            hasuser: "/api/hasuser",
            add_knowledges: "/api/add_knowledges",
            knowledges: "/api/knowledges",
            publish_knowledge: "/api/publish_knowledge",
            qas: "/api/qas",
            sessions: "/api/sessions",
            add_session: "/api/add_session",
            history: "/api/history"
        },
        post: {
            login: "/api/login",
            signup: "/api/signup",
            upload_file: "/api/upload_file",
            updateknowledge: "/api/updateknowledge",
            qa: "/api/qa",
            chat: "/api/chat"
        }
    }
}