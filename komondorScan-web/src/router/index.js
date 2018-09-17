import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '../store'
import Cookies from 'js-cookie'

Vue.use(VueRouter)

function load(component) {
    return () => System.import(`../views/${component}.vue`)
}

const router = new VueRouter({
    /*
     * NOTE! VueRouter "history" mode DOESN'T works for Cordova builds,
     * it is only to be used only for websites.
     *
     * If you decide to go with "history" mode, please also open /config/index.js
     * and set "build.publicPath" to something other than an empty string.
     * Example: '/' instead of current ''
     *
     * If switching back to default "hash" mode, don't forget to set the
     * build publicPath back to '' so Cordova builds work again.
     */

    routes: [{
        path: '/',
        component: load('Index-layout'),
        navName: '任务列表',
        navIcon: 'fa-list-alt',
        hasSub: false,
        children: [{
            path: '',
            component: load('TaskList')
        }]
    }, {
        path: '/tasks/add',
        component: load('Index-layout'),
        navName: '创建任务',
        navIcon: 'fa-plus',
        hasSub: false,
        children: [{
            path: '',
            component: load('CreateTask')
        }]
    }, {
        path: '/pocs',
        component: load('Index-layout'),
        navName: 'POC管理',
        navIcon: 'fa-file-code-o',
        hasSub: false,
        needRole: ['ADMIN'],
        children: [{
            path: '',
            component: load('PocManage')
        }, {
            path: 'add',
            component: load('CreatePoc')
        }]
    }, {
        path: '/poc/:id',
        component: load('Index-layout'),
        children: [{
            path: 'edit',
            component: load('EditPoc')
        }]
    }, {
        path: '/task/:id',
        component: load('Index-layout'),
        children: [{
            path: '',
            component: load('TaskDetail')
        }, {
            path: 'report',
            component: load('TaskLogReport')
        }]
    }, {
        path: '*',
        component: load('error/404')
    }]
})

router.beforeEach((to, from, next) => {
    if (store.state.account.token) {
        next()
    } else {
        if (to.query.accesstoken) {
            store.dispatch('setUserToken', {
                token: to.query.accesstoken,
                func: next
            })
            // next()
        } else if (Cookies.get('token')) {
            store.dispatch('setUserToken', {
                token: Cookies.get('token'),
                func: next
            })
            // next()
        } else {
            let s = `${process.env.AUTH_SERVER_HOST}/login?appid=${process.env.APP_ID}&callback=${encodeURI(process.env.LOCAL_HOST + '/%23' + to.fullPath)}`
            location.href = s
        }
    }
})

export default router
