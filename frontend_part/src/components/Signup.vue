<template>
  <div class="signup">
    <!--注册-->
    <el-card style="width: 480px;margin-left: 33%;margin-top: 8%;background-color: #F4F8FB">
      <div slot="header" class="clearfix">
        <span style="color: cornflowerblue;font-size: 16px">注册</span>
      </div>
      <el-form :model="signupForm">
        <el-form-item label="注册邮箱" label-width="80px">
          <el-input v-model="signupForm.email" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>

        <el-form-item label="用户名" label-width="80px">
          <el-input v-model="signupForm.username" style="margin-left: 5%;width: 80%;"
                    clearable></el-input>
        </el-form-item>

        <div style="margin-left: 27%">
            <span style="margin-right: 50px">
              <el-button style="">取消</el-button>
            </span>
          <span>
              <el-button type="primary" @click="signUp">注册</el-button>
            </span>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import api from '../api/index'
import {signUpUser} from '../api/url.js'

export default {
  name: 'signup',
  data () {
    return {
      errMsg: '',
      signupForm: {
        email: '',
        username: ''
      }
    }
  },
  methods: {
    async signUp () {
      // 数据校验 todo 正则表达式
      // if (this.signupForm.email !== '') {
      //   let obj = this.signupForm.email
      //   let reg = new RegExp('^(\\w-*\\.*)+@(\\w-?)+(\\.\\w{2,})+$')
      //   if (!reg.test(obj.value)) {
      //     this.$message({type: 'warning', message: 'Email 格式有误！', duration: 2000})
      //     return false
      //   }
      // }
      if (this.signupForm.email === '') {
        this.$message({type: 'warning', message: 'Email不能为空！', duration: 2000})
        return false
      }
      if (this.signupForm.username === '') {
        this.$message({type: 'warning', message: 'Username不能为空！', duration: 2000})
        return false
      }
      let params = {
        email: this.signupForm.email,
        username: this.signupForm.username
      }
      const response = await api.post(signUpUser, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Success', duration: 2000})
        this.$router.push({path: '/login'})
      } else {
        this.$message({type: 'error', message: 'Failed', duration: 2000})
      }
    }
  },
  watch: {}
}
</script>

<style scoped>
</style>
