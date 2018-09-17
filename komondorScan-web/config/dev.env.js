var merge = require('webpack-merge')
var prodEnv = require('./prod.env')

module.exports = merge(prodEnv, {
    NODE_ENV: '"development"',
    LOCAL_HOST: '"http://localhost:8080"',
    AUTH_SERVER_HOST: '"http://192.168.7.60:6200"',
    APP_ID: '"3d0ca0517d9211e7bc3fac87a304fa2e"',
    API_HOST: '"http://192.168.7.60:6216"',
    APP_NAME: '"KomondorScan"'
})
