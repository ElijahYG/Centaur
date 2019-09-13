<template>
  <div class="signup">
    <!--修改密码-->
    <el-card style="width: 480px;margin-left: 33%;margin-top: 8%;background-color: #F4F8FB">
      <div slot="header" class="clearfix">
        <span style="color: cornflowerblue;font-size: 16px">修改密码</span>
      </div>
      <el-form :model="changePass">
        <el-form-item label="用户名" label-width="80px">
          <el-input v-model="changePass.username" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>

        <el-form-item label="原密码" label-width="80px">
          <el-input v-model="changePass.oldPass" style="margin-left: 5%;width: 80%;"
                    clearable></el-input>
        </el-form-item>

        <el-form-item label="新密码" label-width="80px">
          <el-input v-model="changePass.newPass" style="margin-left: 5%;width: 80%;"
                    clearable></el-input>
        </el-form-item>

        <div style="margin-left: 27%">
            <span style="margin-right: 50px">
              <el-button style="">取消</el-button>
            </span>
          <span>
              <el-button type="primary" @click="confirmChange">确定</el-button>
            </span>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import api from '../api/index'
import {changePassword} from '../api/url.js'

export default {
  name: 'signup',
  data () {
    return {
      changePass: {
        username: '',
        oldPass: '',
        newPass: ''
      }
    }
  },
  methods: {
    async confirmChange () {
      // 密码校验
      if (this.changePass.oldPass === this.changePass.newPass) {
        this.$message({type: 'warning', message: '新密码与原密码一致，请修改！', duration: 2000})
      }
      if (this.changePass.username === '') {
        this.$message({type: 'warning', message: 'Username不能为空！', duration: 2000})
        return false
      }
      if (this.changePass.oldPass === '') {
        this.$message({type: 'warning', message: '原密码不能为空！', duration: 2000})
        return false
      }
      if (this.changePass.newPass === '') {
        this.$message({type: 'warning', message: '新密码不能为空！', duration: 2000})
        return false
      }
      let params = {
        username: this.changePass.username,
        oldpassword: this.changePass.oldPass,
        newpassword: this.changePass.newPass
      }
      const response = await api.post(changePassword, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Success', duration: 2000})
        this.clearCookie()
        this.$router.push({path: '/login'})
      } else {
        this.$message({type: 'error', message: 'Failed', duration: 2000})
      }
    },
    // 清除cookies
    clearCookie () {
      if (this.$cookies.isKey('userCookie')) {
        this.$cookies.remove('userCookie')
      }
    }
  },
  watch: {}
}
</script>

<style scoped>
</style>
