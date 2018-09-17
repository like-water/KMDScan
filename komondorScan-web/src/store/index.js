import Vue from 'vue'
import Vuex from 'vuex'
import * as actions from './actions'
import * as getters from './getters'
import account from './modules/account'

Vue.use(Vuex)

export default new Vuex.Store({
    actions,
    getters,
    modules: {
        account
    },
    strict: process.env.NODE_ENV !== 'production'
})
