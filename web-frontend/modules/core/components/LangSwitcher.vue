<template>
  <Dropdown v-model="language" :show-search="false" class="language-switcher">
    <DropdownItem
      v-for="locale in $i18n.locales"
      :key="locale.code"
      :name="locale.name"
      :value="locale.code"
    ></DropdownItem>
  </Dropdown>
</template>

<script>
export default {
  name: 'LanguageSwitcher',
  props: {},
  data() {
    return {
      language: this.$i18n.locale,
    }
  },
  watch: {
    language(newLang) {
      this.$i18n.setLocale(newLang)
    },
  },
}
</script>
