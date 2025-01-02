import axios from 'axios'
import config from '@/config'


let get = async (path: string) => {
    return await axios.get(config.host + path)
}
let post = async (path: string, formData: object) => {
    return await axios.post(config.host + path, formData, config.headers)
}
let postfile = async (path: string, formData: object) => {
    return await axios.post(config.host + path, formData, {
        headers: {
            "Access-Control-Allow-Origin": "*", "Content-Type": "multipart/form-data"
        }
    },)
}

export { get, post ,postfile}
