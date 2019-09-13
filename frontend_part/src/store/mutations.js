import types from './mutation_types'

const mutations = {
  [types.SET_USERINFO] (state, userinfo) {
    state.userInfoStore = userinfo
  }
}
export default mutations
