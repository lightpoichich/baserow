<template>
  <Dropdown
    ref="dropdown"
    :value="value"
    :show-search="false"
    v-bind="$attrs"
    @change="handleDropdownChange($event)"
  >
    <DropdownItem
      v-for="(locale, index) in $i18n.locales"
      :key="locale.code"
      :ref="`dropdownItem${index}`"
      :name="locale.name"
      :value="locale.code"
    ></DropdownItem>
  </Dropdown>
</template>

<script>
import Dropdown from "@baserow/modules/core/components/Dropdown";
import DropdownItem from "@baserow/modules/core/components/DropdownItem";

export default {
  components: { Dropdown, DropdownItem },
  name: "LanguageSwitcherDropdown",
  data() {
    return {
      value: this.$i18n.locale,
    };
  },
  methods: {
    toggle(...args) {
      return this.$refs.dropdown.toggle(...args);
    },
    handleDropdownChange(value) {
      this.value = value;
      this.$i18n.setLocale(value);
    },
  },
};
</script>
