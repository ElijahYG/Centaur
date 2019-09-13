import Vue from 'vue'
import Router from 'vue-router'
import VueCookies from 'vue-cookies'
import Home from '@/components/Home'
import Login from '@/components/Login'
import Signup from '@/components/Signup'
import ChangePassword from '@/components/ChangePassword'
import AuthManagement from '@/components/AuthManagement'
import subMenu01 from '@/components/subMenu01'
import Sample01 from '@/components/Samples/Sample01'


Vue.use(Router)
Vue.use(VueCookies)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/signup',
      name: 'Signup',
      component: Signup
    },
    {
      path: '/change_password',
      name: 'ChangePassword',
      component: ChangePassword
    },
    {
      path: '/auth_management',
      name: 'AuthManagement',
      component: AuthManagement
    },
    {
      path: '/testMenu/subMenu01',
      name: 'subMenu01',
      component: subMenu01
    },
    {
      path: '/sampleMenu/sample01',
      name: 'Sample01',
      component: Sample01
    }
  ]
})

// 全局导航守卫
router.beforeEach(async (to, from, next) => {
  if (to.path === '/login' || to.path === '/signup') {
    next()
  } else {
    let curUser = Vue.cookies.get('userCookie')
    console.log('当前cookies：' + curUser)
    if (curUser === '' || curUser === null) {
      next({
        path: '/login',
        query: {next: to.fullPath}
      })
    } else {
      next()
    }
  }
})
export default router
