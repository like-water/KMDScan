const Host = process.env.API_HOST

export default {
    getUserByToken: Host + '/api/userinfo',
    pocs: Host + '/api/pocs',
    poc: pocID => Host + '/api/poc/' + pocID,
    tasks: Host + '/api/tasks',
    task: taskID => Host + '/api/task/' + taskID,
    pocsForSelect: Host + '/api/select/pocs',
    taskLog: taskID => Host + '/api/tasklog/' + taskID
}
