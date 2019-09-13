<template>
  <div class="home">
    <font color="green" size="18" style="font-weight:bold">{{msg}}</font>
  </div>
</template>

<script>
  import {mapGetters} from 'vuex'

  export default {
    name: 'Home',
    data() {
      return {
        msg: 'Centaur'
      }
    },
    computed: {
      ...mapGetters(['setApp'])
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .home {
    padding-top: 180px;
    text-align: center;
  }

</style>
