/**
 *  js公共方法
 */

// 字符串模版函数
export function str (strings = '', ...keys) {
  return function (...values) {
    var dict = values[values.length - 1] || {}
    var result = [strings[0]]
    keys.forEach(function (key, i) {
      var value = Number.isInteger(key) ? values[key] : dict[key]
      result.push(value, strings[i + 1])
    })
    return result.join('')
  }
}

// 分离出object部分属性
export function partObj (obj, ...args) {
  let newObj = {}
  args.forEach(function (arg) {
    if (arg.indexOf('.') !== -1) { // 取最里面的一层对象
      let keys = arg.split('.')
      let keyObj = Object.assign({}, obj)
      keys.forEach(function (key) {
        keyObj = keyObj[key]
      })
      newObj[keys[1]] = keyObj
    } else {
      newObj[arg] = obj[arg] || ''
    }
  })
  return newObj
}

// 去掉字符串前后空格
export function trimStr (str) {
  return str.replace(/(^\s*)|(\s*$)/g, '')
}

// 格式化日期(date: new Date() fmt: yyyy-MM-dd hh:mm:ss.S)
export function dateFmt (date, fmt) {
  if (!date) {
    return ''
  }
  let o = {
    'M+': date.getMonth() + 1,
    'd+': date.getDate(),
    'h+': date.getHours(),
    'm+': date.getMinutes(),
    's+': date.getSeconds(),
    'q+': Math.floor((date.getMonth() + 3) / 3),
    'S': date.getMilliseconds()
  }
  if (/(y+)/.test(fmt)) {
    fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
  }
  for (var k in o) {
    if (new RegExp('(' + k + ')').test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
    }
  }
  return fmt
}

export function isEmpty (value) {
  if (isNaN(value)) { // 非数字
    return (value == null || value.toString().length === 0 || Object.keys(value).length === 0) // "" [] {} null undefined
  } else { // 注意！数字(包括0)全部返回非空
    return false
  }
}

export function cloneObj (obj) {
  let str
  let newobj = obj.constructor === Array ? [] : {}
  if (typeof obj !== 'object') {
    return
  } else if (window.JSON) {
    str = JSON.stringify(obj) // 系列化对象
    newobj = JSON.parse(str) // 还原
  } else {
    for (var i in obj) {
      newobj[i] = typeof obj[i] === 'object' ? cloneObj(obj[i]) : obj[i]
    }
  }
  return newobj
}

// 判断
export function isOwnEmpty (obj) {
  for (var name in obj) {
    if (obj.hasOwnProperty(name)) {
      return false
    }
  }
  return true
}
