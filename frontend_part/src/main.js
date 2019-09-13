// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import Vuex from 'vuex'
import store from './store/index'
import Index from './Index'
import router from './router'
// import iview
import {
  Menu,
  MenuItem,
  Submenu,
  MenuGroup,
  Breadcrumb,
  BreadcrumbItem,
  Modal,
  Button,
  Select,
  Option,
  Icon
} from 'iview'
import 'iview/dist/styles/iview.css'
// import element-ui
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import vue-cookies
import VueCookies from 'vue-cookies'

Vue.use(Vuex)
Vue.use(VueCookies)
Vue.use(ElementUI)
Vue.config.productionTip = false

// iview components
// the first parameter of vue.components means the component name, which can be self-defined especially when component names are conflicted
Vue.component('Menu', Menu)
Vue.component('MenuItem', MenuItem)
Vue.component('Submenu', Submenu)
Vue.component('MenuGroup', MenuGroup)
Vue.component('Breadcrumb', Breadcrumb)
Vue.component('BreadcrumbItem', BreadcrumbItem)
Vue.component('Modal', Modal)
Vue.component('IviewBtn', Button)
Vue.component('IviewSelect', Select)
Vue.component('IviewOption', Option)
Vue.component('Icon', Icon)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {Index},
  template: '<Index/>',
  data: {
    Hub: new Vue()
  }
})
