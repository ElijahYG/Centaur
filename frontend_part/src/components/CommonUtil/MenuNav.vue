<template>
  <div style="display: inline">
    <template v-for="(value, key, index) in data">
      <template v-if="!value.hide">
        <template v-if="value.sub && value.sub.length !== 0">
          <MenuGroup v-if="fatherName"
                     :title="value.desc" :key="key+'1'">
            <menu-nav :data="value.sub"
                      :fatherName="computeName(index)"
                      :fatherLink="computeLink(key)">
            </menu-nav>
          </MenuGroup>
          <Submenu v-else
                   :name="computeName(key)" :key="key+'2'">
            <template slot="title">
              <Icon :type="value.icon"></Icon>
              {{ value.desc }}
            </template>
            <menu-nav :data="value.sub"
                      :fatherName="computeName(index)"
                      :fatherLink="computeLink(key)">
            </menu-nav>
          </Submenu>
        </template>
        <a v-else-if="value.customLink" :href="value.href" :key="key+'3'">
          <menuItem :name="computeName(index)">
            <Icon v-if="value.icon" :type="value.icon"></Icon>
            {{ value.desc }}
          </menuItem>
        </a>
        <router-link v-else :to="computeLink(key)" :key="key+'4'">
          <menuItem :name="computeName(index)">
            <Icon v-if="value.icon" :type="value.icon" :key="key+'5'"></Icon>
            {{ value.desc }}
          </menuItem>
        </router-link>
      </template>
    </template>
  </div>
</template>

<script>
export default {
  name: 'menuNav',
  props: ['data', 'fatherName', 'fatherLink'],
  methods: {
    computeName: function (index) {
      if (this.fatherName) {
        return `${this.fatherName}-${index + 1}`
      } else {
        return `${index + 1}`
      }
    },
    computeLink: function (key) {
      if (this.fatherLink) {
        return `${this.fatherLink}/${key}`
      } else {
        return `/${key}`
      }
    }
  }
}
</script>
