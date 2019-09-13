<template>
  <div class="hello">
    <h3 style="text-align: center">菜单一</h3>
    <div style="text-align: center;margin-top: 5%">
      <el-button @click="testGetUsers" type="primary" plain>点击测试权限</el-button>
    </div>
  </div>
</template>

<script>
import api from '../api/index'
import {testGetUsers} from '../api/url.js'

export default {

  name: 'subMenu01',
  data () {
    return {}
  },
  methods: {
    async testGetUsers () {
      const response = await api.get(testGetUsers, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Group List Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Get Group List Failed', duration: 2000})
      }
    }
  },
  created: function () {
    this.testGetUsers()
  }
}
</script>

<style scoped>
</style>
