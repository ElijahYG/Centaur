import axios from 'axios'
import qs from 'qs'
import router from '../router'
import {Message, LoadingBar} from 'iview'
import {BASEURL} from '../config.js'

// 请求时拦截器
axios.interceptors.request.use(
  config => {
    LoadingBar.start()
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 请求后的拦截器
axios.interceptors.response.use(
  response => response,
  error => Promise.resolve(error.response)
)

// 检查http状态
function checkStatus (response) {
  if (response && (response.status === 200 || response.status === 304)) {
    LoadingBar.finish()
    return response.data
  } else {
    LoadingBar.error()
    return {
      data: {
        status: 404
        // msg: response.statusText,
        // data: response.statusText
      }
    }
  }
}

// 检查数据中自定义的数据状态
function checkDataStatus (res) {
  if (parseInt(res.status) === 200) { // 200 正常返回数据
    return res
  } else if (parseInt(res.status) === 302) { // 300 重定向到登录界面
    Message.destroy()
    Message.warning('<p>请先登录</p>' + '<p>Please Login in before you access this page</p>')
    router.push({path: '/login'})
  } else if (parseInt(res.status) === 403) { // 403 跳转到权限页面
    Message.destroy()
    Message.warning({
      content: '<p>您没有此权限，请先开通权限</p>' + '<p>You are forbidden to access this page without authentication</p>',
      closable: true,
      duration: 10
    })
  } else { // 其他错误返回，以后处理
    return res
  }
}

// 封装请求
export default {
  post (url, data) {
    return axios({
      method: 'post',
      url: BASEURL + url,
      // 如果用FormData格式传文件,则不能用qs序列化
      data: data.constructor !== FormData ? qs.stringify(data) : data,
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
      }
    }).then(checkStatus).then(checkDataStatus)
  },
  get (url, params) {
    return axios({
      method: 'get',
      url: BASEURL + url,
      params,
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    }).then(checkStatus).then(checkDataStatus)
  },
  // 当请求头里设置Content-Type:application/json，参数会显示在Request payload块里提交。
  // 该方法为了兼容Django后端通过json.loads获取请求参数
  postByPayload (url, data) {
    return axios({
      method: 'post',
      url: BASEURL + url,
      data: JSON.stringify(data),
      timeout: 30000,
      headers: {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json;charset=UTF-8'
      }
    }).then(checkStatus).then(checkDataStatus)
  }
}
