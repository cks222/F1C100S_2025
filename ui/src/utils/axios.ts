import axios from 'axios'
import config from '@/config'
let get = async (path: string) => {
    let response = await axios.get(config.host + path)
    return response.data;
}
let post = async (path: string, formData: object) => {
    let response = await axios.post(config.host + path, formData, config.headers)
    return response.data;
}
let postfile = async (path: string, formData: object) => {
    let response = await axios.post(config.host + path, formData, {
        headers: {
            "Access-Control-Allow-Origin": "*", "Content-Type": "multipart/form-data"
        }
    },)
    return response.data;
}
async function api_login(account: string, token: string) {
    let data = new FormData();
    data.append("account", account);
    data.append("token", token);
    return await post("/api/login", data)
}
async function api_login_byid(userid: string, token: string) {
    let data = new FormData();
    data.append("userid", userid);
    data.append("token", token);
    return await post("/api/login_byid", data)
}
async function api_getuser_byid(userid: string) {
    return await get("/api/get_user?userid=" + userid)
}
async function check_user(userid: string, token: string) {
    let data = new FormData();
    data.append("userid", userid);
    data.append("token", token);
    return await post("/api/check_user", data)
}
async function api_has_account(account: string) {
    return await get("/api/has_account?account=" + account)
}
async function api_signup(account: string, token: string) {
    let data = new FormData();
    data.append("account", account);
    data.append("token", token);
    return await post("/api/signup", data)
}
async function api_upload_file(knowledgeid: string, data: FormData) {
    return await post("/api/upload_file?knowledgeid=" + knowledgeid, data)
}
async function get_api_addknowledges(userid: string, knowledgename: string, ispublic: boolean) {
    return await get("/api/add_knowledges?userid=" + userid + "&knowledgename=" + knowledgename + "&ispublic=" + ispublic)
}
async function get_api_knowledges(userid: string, containspublic: boolean) {
    return await get("/api/knowledges?userid=" + userid + "&containspublic=" + containspublic)
}
async function get_publish_knowledge(knowledgeid: string) {
    return await get("/api/publish_knowledge?knowledgeid=" + knowledgeid)
}
async function post_api_updateknowledge(knowledgeid: string, knowledge: string) {
    let data = new FormData();
    data.append("knowledge", knowledge);
    return await post("/api/updateknowledge?knowledgeid=" + knowledgeid, data)
}
async function get_api_qas(knowledgeid: string, start: number, count: number) {
    return await get("/api/qas?knowledgeid=" + knowledgeid + "&start=" + start + "&count=" + count)
}
async function post_api_qa(knowledgeid: string, method: string, qas: string) {
    let data = new FormData();
    data.append("qas", qas);
    return await post("/api/qa?knowledgeid=" + knowledgeid + "&method=" + method, data)
}
async function api_sessions(userid: string) {
    return await get("/api/sessions?userid=" + userid)
}
async function api_add_sessions(userid: string, knowledgeid: string) {
    return await get("/api/add_session?userid=" + userid + "&knowledgeid=" + knowledgeid)
}
async function api_del_sessions(sessionid: string) {
    return await get("/api/del_session?sessionid=" + sessionid)
}
async function api_history(sessionid: string) {
    return await get("/api/history?sessionid=" + sessionid)
}
async function api_chat(sessionid: string, history: string, question: string) {
    let data = new FormData();
    data.append("history", history);
    data.append("question", question);
    return await post("/api/chat?usestream=true&sessionid=" + sessionid, data)
}
async function chat_stream_reader (historyid:string){
    const response = await fetch(config.host + '/api/chat_stream?historyid='+historyid);
    return response.body?.getReader();
}
export {
    api_login,
    api_del_sessions,
    api_login_byid,
    api_getuser_byid,
    check_user,
    api_has_account,
    api_signup,
    api_upload_file,
    get_api_addknowledges,
    get_api_knowledges,
    get_publish_knowledge,
    post_api_updateknowledge,
    get_api_qas,
    post_api_qa,
    api_sessions,
    api_add_sessions,
    api_history, api_chat,chat_stream_reader
}
