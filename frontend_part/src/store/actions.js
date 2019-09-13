import types from './mutation_types'

const actions = {
  async setUserInfo ({commit}, userinfo) {
    commit(types.SET_USERINFO, userinfo)
  }
}
export default actions
