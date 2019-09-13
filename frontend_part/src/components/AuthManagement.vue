<template>
  <div class="AuthManagement">
    <!--权限管理-->
    <el-tabs tab-position="left" @tab-click="tabSwitch">
      <el-tab-pane label="用户列表" name="user_list" lazy>
        <template>
          <el-table :data="userListTable" stripe style="width: 90%;margin-left: 3%">
            <el-table-column prop="id" label="序号" width="100"></el-table-column>
            <el-table-column prop="username" label="用户名"></el-table-column>
            <el-table-column prop="last_login" label="最后登录时间"></el-table-column>
            <el-table-column prop="email" label="邮箱"></el-table-column>
            <el-table-column prop="is_active" label="是否激活"></el-table-column>
            <el-table-column prop="is_superuser" label="是否管理员"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <div style="margin-bottom: 2%">
                  <el-button size="mini" @click="showUserGroupDialog(scope.row)" type="primary">用户组分配</el-button>
                </div>

                <div v-if="scope.row.is_active === 'True'" style="margin-bottom: 1%">
                  <el-button size="mini" @click="switchUserStatus(scope.row)" type="warning">冻结</el-button>
                </div>
                <div v-else style="margin-bottom: 2%">
                  <el-button size="mini" @click="switchUserStatus(scope.row)" type="success">激活</el-button>
                </div>

                <div>
                  <el-button size="mini" @click="delhUser(scope.row)" type="danger">刪除</el-button>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-tab-pane>

      <el-tab-pane label="权限列表" name="permission_list" lazy>
        <div>
          <el-button type="success" @click="showAddPermissionDialog" plain style="margin-left: 3%">添加权限</el-button>
        </div>
        <template>
          <el-table :data="permissionListTable" stripe style="width: 90%;margin-left: 3%">
            <el-table-column prop="id" label="序号" width="100"></el-table-column>
            <el-table-column prop="codename" label="权限名(api)"></el-table-column>
            <el-table-column prop="name" label="权限说明"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" @click="delPermission(scope.row.id)" type="danger">刪除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-tab-pane>

      <el-tab-pane label="分组列表" name="group_list" lazy>
        <div>
          <el-button type="success" @click="showAddGroupDialog" plain style="margin-left: 3%">添加分组</el-button>
        </div>
        <template>
          <el-table :data="groupListTable" stripe style="width: 90%;margin-left: 3%">
            <el-table-column prop="id" label="序号" width="100"></el-table-column>
            <el-table-column prop="name" label="组名"></el-table-column>
            <el-table-column label="操作">
              <template slot-scope="scope">
                <el-button size="mini" @click="showGroupPerDialog(scope.row.id)" type="primary">组权限分配</el-button>
                <el-button size="mini" @click="delGroup(scope.row.id)" type="danger">刪除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-tab-pane>
    </el-tabs>

    <!--组权限分配对话框-->
    <el-dialog title="组权限管理" :visible.sync="groupPerDialog" @close="closeGroupPerDialog">
      <div style="margin-left: 13%">
        <el-transfer
          filterable
          :filter-method="filterMethod"
          filter-placeholder="输入权限名搜索"
          :titles="['未获得权限', '已获得权限']"
          v-model="ownPerList"
          :data="allPerList">
        </el-transfer>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="closeGroupPerDialog">取消</el-button>
        <el-button type="primary" @click="dispatchPer">确定</el-button>
      </span>
    </el-dialog>

    <!--添加权限组对话框-->
    <el-dialog title="添加权限组" :visible.sync="addGroupDialog" width="600px">
      <el-form :model="addGroupForm">
        <el-form-item label="权限组名称" label-width="100px">
          <el-input v-model="addGroupForm.name" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="addGroupDialog = false">取消</el-button>
        <el-button type="primary" @click="addGroup">确定</el-button>
      </span>
    </el-dialog>

    <!--添加权限对话框-->
    <el-dialog title="添加权限" :visible.sync="addPermissionDialog" width="600px">
      <el-form :model="addPermissionForm">
        <el-form-item label="权限名" label-width="100px">
          <el-input v-model="addPermissionForm.codename" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>

        <el-form-item label="权限说明" label-width="100px">
          <el-input v-model="addPermissionForm.name" style="margin-left: 5%;width: 80%;" clearable></el-input>
        </el-form-item>

        <el-form-item label="所属应用" label-width="100px">
          <el-select v-model="addPermissionForm.appId" placeholder="请选择" style="margin-left: 5%;width: 80%;">
            <el-option
              v-for="app in appList"
              :key="app.id"
              :label="app.label"
              :value="app.id">
            </el-option>
          </el-select>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button @click="addPermissionDialog = false">取消</el-button>
        <el-button type="primary" @click="addPermission">确定</el-button>
      </span>
    </el-dialog>

    <!--用户组分配对话框-->
    <el-dialog title="用户组管理" :visible.sync="userGroupDialog" @close="closeUserGroupDialog">
      <div style="margin-left: 13%">
        <el-transfer
          filterable
          :filter-method="filterMethod"
          filter-placeholder="输入组名搜索"
          :titles="['未分配组', '已分配组']"
          v-model="ownGroupList"
          :data="allGroupList">
        </el-transfer>
      </div>

      <span slot="footer" class="dialog-footer">
        <el-button @click="closeUserGroupDialog">取消</el-button>
        <el-button type="primary" @click="dispatchGroup">确定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import api from '../api/index'
import {
  getUserList,
  getPermissionList,
  getGroupList,
  getGroupPermissionList,
  modUserStatus,
  modGroupPermissionList,
  delGroupItem,
  addGroupItem,
  getContentTypeList,
  addPermissionItem,
  delPermissionItem,
  delUserItem,
  modUserGroupList,
  getUserGroupList
} from '../api/url.js'

export default {
  name: 'AuthManagement',
  data () {
    return {
      userListTable: [],
      permissionListTable: [],
      groupListTable: [],
      groupPerDialog: false,
      addGroupDialog: false,
      addPermissionDialog: false,
      allPerList: [],
      ownPerList: [],
      userGroupDialog: false,
      allGroupList: [],
      ownGroupList: [],
      groupId: '',
      userId: '',
      addGroupForm: {
        name: ''
      },
      addPermissionForm: {
        name: '',
        codename: '',
        appId: '' // content type id
      },
      appList: []
    }
  },
  methods: {
    // 切换左边栏
    tabSwitch (tab) {
      if (tab.name === 'user_list') {
        this.getUserList()
      }
      if (tab.name === 'permission_list') {
        this.getPermissionList()
      }
      if (tab.name === 'group_list') {
        this.getGroupList()
      }
    },
    // 获取用户列表
    async getUserList () {
      const response = await api.get(getUserList, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get User List Success', duration: 2000})
        this.userListTable = response.data
      } else {
        this.$message({type: 'error', message: 'Get User List Failed', duration: 2000})
      }
    },
    // 获取权限列表
    async getPermissionList () {
      const response = await api.get(getPermissionList, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Permission List Success', duration: 2000})
        this.permissionListTable = response.data
      } else {
        this.$message({type: 'error', message: 'Get Permission List Failed', duration: 2000})
      }
    },
    // 获取组列表
    async getGroupList () {
      const response = await api.get(getGroupList, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Group List Success', duration: 2000})
        this.groupListTable = response.data
      } else {
        this.$message({type: 'error', message: 'Get Group List Failed', duration: 2000})
      }
    },
    // 获取组权限列表
    async getGroupPermissionList (id) {
      const response = await api.get(getGroupPermissionList, {id: id})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Group Permission List Success', duration: 2000})
        this.allPerList = response.data.all_per_list
        this.ownPerList = response.data.own_per_list
      } else {
        this.$message({type: 'error', message: 'Get Group Permission List Failed', duration: 2000})
      }
    },
    // 用户激活/冻结
    async switchUserStatus (row) {
      let params = {
        id: row.id,
        active: row.is_active === 'False' ? 'True' : 'False'
      }
      const response = await api.get(modUserStatus, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Switch User Status Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Switch User Status Failed', duration: 2000})
      }
      this.getUserList()
    },
    // 组权限对话框打开
    showGroupPerDialog (id) {
      this.groupId = id
      this.getGroupPermissionList(id)
      this.groupPerDialog = true
    },
    // 组权限对话框关闭
    closeGroupPerDialog () {
      this.groupId = ''
      this.allPerList = []
      this.ownPerList = []
      this.groupPerDialog = false
    },
    // 提交组权限分配
    async dispatchPer () {
      let params = {
        group_id: this.groupId,
        own_per_list: JSON.stringify(this.ownPerList)
      }
      const response = await api.get(modGroupPermissionList, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Modify Group Permission List Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Modify Group Permission List Failed', duration: 2000})
      }
      this.groupId = ''
      this.groupPerDialog = false
    },
    // 组权限穿梭框筛选
    filterMethod (query, item) {
      return item.label.indexOf(query) > -1
    },
    // 删除权限组
    async delGroup (id) {
      let params = {
        group_id: id
      }
      const response = await api.get(delGroupItem, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Delete Group Item Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Delete Group Item Failed', duration: 2000})
      }
      this.groupPerDialog = false
      this.getGroupList()
    },
    // 显示添加权限组对话框
    showAddGroupDialog () {
      this.addGroupForm = {
        name: ''
      }
      this.addGroupDialog = true
    },
    // 添加权限组
    async addGroup () {
      let params = {
        name: this.addGroupForm.name
      }
      const response = await api.get(addGroupItem, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Add Group Item Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Add Group Item Failed', duration: 2000})
      }
      this.addGroupDialog = false
      this.getGroupList()
    },
    // 显示添加权限对话框
    showAddPermissionDialog () {
      this.addPermissionForm = {
        name: ''
      }
      this.getContentType()
      this.addPermissionDialog = true
    },
    // 获取所有的content type，用于添加权限
    async getContentType () {
      const response = await api.get(getContentTypeList, {})
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Content Type List Success', duration: 2000})
        this.appList = response.data
      } else {
        this.$message({type: 'error', message: 'Get Content Type List Failed', duration: 2000})
      }
    },
    // 添加权限
    async addPermission () {
      let params = {
        name: this.addPermissionForm.name,
        codename: this.addPermissionForm.codename,
        app_id: this.addPermissionForm.appId
      }
      const response = await api.get(addPermissionItem, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Add Permission Item Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Add Permission Item Failed', duration: 2000})
      }
      this.getPermissionList()
      this.addPermissionDialog = false
    },
    // 删除权限
    async delPermission (id) {
      let params = {
        permission_id: id
      }
      const response = await api.get(delPermissionItem, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Delete Permission Item Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Delete Permission Item Failed', duration: 2000})
      }
      this.getPermissionList()
    },
    // 删除用户
    async delhUser (row) {
      let params = {
        id: row.id
      }
      this.$confirm('确定要删除该用户吗？', '删除用户', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const response = await api.get(delUserItem, params)
        if (parseInt(response.status) === 200) {
          this.$message({type: 'success', message: 'Delete User Item Success', duration: 2000})
        } else {
          this.$message({type: 'error', message: 'Delete User Item Failed', duration: 2000})
        }
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '取消',
          duration: 1000
        })
      })
    },
    // 用户组分配对话框打开
    showUserGroupDialog (row) {
      this.userId = row.id
      if (row.is_superuser === 'True') {
        this.$message({type: 'warning', message: 'Current User is Superuser!', duration: 5000})
        return false
      } else {
        this.getUserGroupList(row.id)
      }
      this.userGroupDialog = true
    },
    // 获取用户组列表
    async getUserGroupList (id) {
      let params = {
        user_id: id
      }
      const response = await api.get(getUserGroupList, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Get Uesr Group Success', duration: 2000})
        this.allGroupList = response.data.all_group_list
        this.ownGroupList = response.data.own_group_list
      } else {
        this.$message({type: 'error', message: 'Get Uesr Group Failed', duration: 2000})
      }
      this.getUserList()
    },
    // 用户组对话框关闭
    closeUserGroupDialog () {
      this.userId = ''
      this.allGroupList = []
      this.ownGroupList = []
      this.userGroupDialog = false
    },
    // 提交用户组分配
    async dispatchGroup () {
      let params = {
        user_id: this.userId,
        own_group_list: JSON.stringify(this.ownGroupList)
      }
      const response = await api.get(modUserGroupList, params)
      console.log(response)
      if (parseInt(response.status) === 200) {
        this.$message({type: 'success', message: 'Modify User Group List Success', duration: 2000})
      } else {
        this.$message({type: 'error', message: 'Modify User Group List Failed', duration: 2000})
      }
      this.userId = ''
      this.userGroupDialog = false
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
