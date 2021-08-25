<template>
  <div>
    <a
      ref="dropdownLink"
      class="lang-picker"
      @click="$refs.dropdown.toggle($refs.dropdownLink)"
    >
      {{ visibleLanguageName }}
      <i class="fa fa-caret-down lang-picker__icon"></i>
    </a>
    <LanguageSwitcherDropdown ref="dropdown" :show-input="false" />
  </div>
</template>

<script>
import LanguageSwitcherDropdown from '@baserow/modules/core/components/LangSwitcherDropdown'

export default {
  components: { LanguageSwitcherDropdown },
  computed: {
    visibleLanguageName() {
      for (let i = 0; i < this.$i18n.locales.length; i++) {
        if (this.$i18n.locales[i].code === this.$i18n.locale) {
          return this.$i18n.locales[i].name
        }
      }
      return ''
    },
  },
}
</script>
