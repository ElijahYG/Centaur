<template>
  <div id="app">
    <div v-if="userCookie === '' || userCookie == null">
      <div class="menu">
        <div class="left">
          <a href="/" class="layout-logo">
            <img src="./assets/logo.png" height="50px" width="50px" style="margin-top: -10px">
          </a>
        </div>
        <div class="middle-space"></div>
        <Menu mode="horizontal" theme="light" class="layout-nav-menu">
          <div class="layout-nav">
            <Submenu name="300" class="menu-log">
              <template slot="title">
                {{ 'Anonymous' }}
              </template>
              <div>
                <MenuItem name="300-1"  @click.native="createUser">{{"注册"}}</MenuItem>
              </div>
              <!--<div>-->
                <!--<MenuItem name="300-2" @click.native="changePassword">{{"修改密码"}}</MenuItem>-->
              <!--</div>-->
              <!--<div>-->
                <!--<MenuItem @click.native="userLogout" name="300-3">{{"登出"}}</MenuItem>-->
              <!--</div>-->
              <!--<div v-if="userInfo.is_superuser">-->
                <!--<MenuItem name="300-4">{{"权限管理"}}</MenuItem>-->
              <!--</div>-->
            </Submenu>
          </div>
        </Menu>
      </div>
      <!--Login视图-->
      <router-view class="login"></router-view>
    </div>
    <div v-else>
      <div class="menu">
        <div class="left">
          <a href="/">
            <el-button type="primary" style="margin-left: 10px;margin-top:10px;" icon="el-icon-back" round></el-button>
          </a>
        </div>
        <div class="middle-space"></div>
        <Menu mode="horizontal" theme="light" class="layout-nav-menu">
          <div class="layout-nav">
            <MenuNav :data="getMenuDesc" father-link=""></MenuNav>
            <Submenu name="300" class="menu-log">
              <template slot="title">
                {{userCookie}}
              </template>
              <div>
                <MenuItem name="300-1" @click.native="createUser">{{"注册"}}</MenuItem>
              </div>
              <div>
                <MenuItem name="300-2" @click.native="changePassword">{{"修改密码"}}</MenuItem>
              </div>
              <div>
                <MenuItem @click.native="userLogout" name="300-3">{{"登出"}}</MenuItem>
              </div>
              <div v-if="superUser === 'true'">
                <MenuItem name="300-4" @click.native="authManage">{{"权限管理"}}</MenuItem>
              </div>
            </Submenu>
          </div>
        </Menu>
      </div>
      <div class="layout-content">
        <!--面包屑-->
        <Breadcrumb class="breadcrumb">
          <BreadcrumbItem>
            <router-link to="/">
              {{"主页"}}
            </router-link>
          </BreadcrumbItem>
          <BreadcrumbItem v-for="(BreadcrumbDesc,index) in BreadcrumbDescArr" :key="index+400">
            {{BreadcrumbDesc}}
          </BreadcrumbItem>
        </Breadcrumb>
        <!--渲染视图-->
        <router-view class="view"></router-view>
      </div>
    </div>
  </div>
</template>

<script>
import {menuList} from './config/menu'
import MenuNav from './components/CommonUtil/MenuNav'
import api from './api/index'
import {userLogout} from './api/url.js'

export default {
  data: function () {
    return {
      userInfo: '',
      userCookie: '',
      superUser: 'false'
    }
  },
  components: {MenuNav},
  computed: {
    BreadcrumbDescArr () {
      const pathItemArr = this.$route.path.split('/')
      let menuDict = Object.assign({}, this.getMenuDesc)
      let menuItemArr = []
      for (let i in pathItemArr) {
        const pathItem = pathItemArr[i]
        if (pathItem && isNaN(pathItem) && menuDict.hasOwnProperty(pathItem)) {
          menuItemArr.push(menuDict[pathItem].desc)
          menuDict = menuDict[pathItem].sub
        }
      }
      return menuItemArr
    },
    getMenuDesc () {
      return menuList
    }
  },
  methods: {
    fetchData () {
      this.userCookie = this.$cookies.get('userCookie') // 获取cookie中的当前登录用户名
      this.superUser = this.$cookies.get('isSuperUser') // 获取cookie中的当前登录用户是否是超级用户
      this.userInfo = this.$store.state.userInfoStore // 获取store中的当前登录用户信息
    },
    createUser () {
      this.$router.push({path: '/signup'})
    },
    changePassword () {
      this.$router.push({path: '/change_password'})
    },
    async userLogout () {
      const response = await api.post(userLogout, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Logout Success', duration: 2000})
        this.clearCookie()
        this.$store.dispatch('setUserInfo', '')
        this.$router.push({path: '/login'})
      } else {
        this.$message({type: 'error', message: 'Logout Failed', duration: 2000})
      }
    },
    authManage () {
      this.$router.push({path: '/auth_management'})
    },
    // 清除cookies
    clearCookie () {
      if (this.$cookies.isKey('userCookie')) {
        this.$cookies.remove('userCookie')
        this.userCookie = ''
      }
    }
  },
  created: function () {
    this.fetchData()
  },
  watch: {
    '$route': 'fetchData' // 监控路由，若有变化则执行fetchData方法
  }
}
</script>

<style scoped>
  /* scoped 表示组件内样式 */
  .layout-logo {
    display: inline-block;
    border-radius: 3px;
    margin-top: 16px;
    margin-left: 20px;
  }

  .layout-logo img {
    vertical-align: bottom;
  }

  .layout-nav {
    height: inherit;
    margin-right: 20px;
    display: inline-block;
  }

  .layout-content {
    min-height: 600px;
    margin: 2px 15px 0;
    overflow: hidden;
    border-radius: 4px;
  }

  .menu {
    display: flex;
    justify-content: center;
  }

  .layout-nav-menu {
    flex: none;
  }

  .left {
    width: 48px;
    heigth: 60px;
    border-bottom: 1px solid lightgrey;
  }

  .middle-space {
    width: 10px;
    height: 60px;
    flex: auto;
    border-bottom: 1px solid lightgrey;
  }

  .breadcrumb {
    margin: 10px 8px 10px 8px;
    font-size: 14px;
  }

  /deep/ .layout-nav .ivu-menu-submenu {
    padding: 0 5px;
  }

  @media screen and (min-width: 1440px) {
    /deep/ .layout-nav .ivu-menu-submenu {
      padding: 0 10px;
    }
  }

  @media screen and (min-width: 1680px) {
    /deep/ .layout-nav .ivu-menu-submenu {
      padding: 0 20px;
    }
  }

  /deep/ .ivu-card-body {
    padding: 6px;
  }

  /deep/ li.ivu-menu-item {
    /*padding: 7px 16px 8px!important;*/
    padding: 4px 12px !important;
  }

  .layout-nav-menu {
    z-index: 1999;
  }

  /deep/ .el-loading-mask {
    z-index: 1998;
  }
</style>
