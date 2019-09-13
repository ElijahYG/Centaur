/**
 *
 * Created on 2018/12/27
 * @author: yanggang
 */

function getBaseUrl () {
  if (process.env.NODE_ENV === 'development') {
    return 'http://127.0.0.1:8000'
  }
  console.log('backend BaseUrl: ' + location.origin)
  return location.origin
}

export const BASEURL = getBaseUrl()
