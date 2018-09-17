// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import ElementUI from 'element-ui'
import 'normalize.css'
import 'element-ui/lib/theme-default/index.css'
import 'font-awesome/css/font-awesome.css'
import './assets/main.css'
import VueCodeMirror from 'vue-codemirror'

Vue.use(VueCodeMirror)
// 使用element-ui
Vue.use(ElementUI)

// 发布后是否显示提示
Vue.config.productionTip = false
/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    store,
    template: '<App/>',
    components: {
        App
    }
})
