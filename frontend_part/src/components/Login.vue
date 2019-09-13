<template>
  <div class="login">
    <!--登录-->
    <el-card style="width: 480px;margin-left: 33%;margin-top: 8%;background-color: #F4F8FB">
      <div slot="header" class="clearfix">
        <span style="color: cornflowerblue;font-size: 16px">登录</span>
      </div>
      <el-form :model="loginForm">
        <el-form-item label="用户名" label-width="80px">
          <el-input v-model="loginForm.username" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>

        <el-form-item label="密码" label-width="80px">
          <el-input type="password" v-model="loginForm.password" style="margin-left: 5%;width: 80%;"
                    clearable></el-input>
        </el-form-item>

        <div style="margin-left: 27%">
            <span style="margin-right: 50px">
              <el-button style="">取消</el-button>
            </span>
          <span>
              <el-button type="primary" @click="userLogin">登录</el-button>
            </span>
        </div>
        <div style="margin-top: 10px">
          没有账号？点击 <span style="cursor:pointer;color: cornflowerblue" @click="toSignUp">注册</span>
        </div>
      </el-form>
    </el-card>

  </div>
</template>

<script>
import api from '../api/index'
import {userLogin} from '../api/url.js'

export default {
  name: 'Login',
  data () {
    return {
      next: '',
      loginForm: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async userLogin () {
      let params = {
        username: this.loginForm.username,
        password: this.loginForm.password,
        next: this.$route.query.next
      }
      const response = await api.post(userLogin, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Success', duration: 1200})
        this.$cookies.set('userCookie', response.info.username) // 登录成功后设置用户名cookie
        this.$cookies.set('isSuperUser', response.info.is_superuser) // 登录成功后设置用户是否是超级用户cookie
        this.$store.dispatch('setUserInfo', response.info) // 将用户信息存储在store里
        if (this.$route.query.next === undefined || this.$route.query.next === '') {
          this.$router.push({path: '/'}) // 如果没有next地址就跳转至主页
        } else {
          this.$router.push({path: this.$route.query.next}) // 跳转至登录前访问的url地址
        }
      } else {
        this.$message({type: 'error', message: 'Failed', duration: 1200})
      }
    },
    toSignUp () {
      this.$router.push({path: '/signup'})
    }
  }
}
</script>

<style scoped>
h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
