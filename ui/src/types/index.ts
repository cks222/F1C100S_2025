export interface Session {
    isdisabled: boolean,
    knowledgeid: string,
    sessionid: string,
    username: string,
}

export interface Knowledge {
    username: string,
    id: string,
    knowledgename: string,
    ispublic: boolean,
    currentversion: string,
}


export interface KQA {
    knowledgeid: string,
    QAS: QA[],
}
export interface QA {
    id: string,
    q: string,
    qtime: string,
    a: string,
    atime: string,
    isdisabled: boolean,
}

export interface FileInfo {
    FileName: string,
    Url: string,
    Path: string,
}

export interface SessionHistory {
    SessionId: string,
    Messages: Message[]
}

export interface Message {
    Role: string,
    Content: string,
    Time: string
}
export interface SessionDisplay {
    SessionId: string,
    KnowledgeName: string,
    Q: string,
    QTime: string,
    A: string,
    ATime: string
}