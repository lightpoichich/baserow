<template>
  <div
    class="dropdown"
    :class="{ 'dropdown--floating': !showInput }"
    @contextmenu.stop
  >
    <a v-if="showInput" class="dropdown__selected" @click="show()">
      <div
        v-if="hasValue()"
        class="field-single-select__dropdown-option field-single-select__dropdown-option--align-32"
        :class="'background-color--' + selectedColor"
      >
        {{ selectedName }}
      </div>
      <i class="dropdown__toggle-icon fas fa-caret-down"></i>
    </a>
    <div class="dropdown__items" :class="{ hidden: !open }">
      <div v-if="showSearch" class="select__search">
        <i class="select__search-icon fas fa-search"></i>
        <input
          ref="search"
          v-model="query"
          type="text"
          class="select__search-input"
          :placeholder="searchText"
          @keyup="search(query)"
        />
      </div>
      <ul ref="items" class="select__items" v-prevent-parent-scroll>
        <FieldSingleSelectDropdownItem
          :name="''"
          :value="null"
          :color="''"
        ></FieldSingleSelectDropdownItem>
        <FieldSingleSelectDropdownItem
          v-for="option in options"
          :key="option.id"
          :name="option.value"
          :value="option.id"
          :color="option.color"
        ></FieldSingleSelectDropdownItem>
      </ul>
    </div>
  </div>
</template>

<script>
import dropdown from '@baserow/modules/core/mixins/dropdown'
import FieldSingleSelectDropdownItem from '@baserow/modules/database/components/field/FieldSingleSelectDropdownItem'

export default {
  name: 'FieldSingleSelectDropdown',
  components: { FieldSingleSelectDropdownItem },
  mixins: [dropdown],
  props: {
    options: {
      type: Array,
      required: true,
    },
  },
  computed: {
    selectedColor() {
      return this.getSelectedProperty(this.value, 'color')
    },
  },
  methods: {
    forceRefreshSelectedValue() {
      this._computedWatchers.selectedColor.run()
      dropdown.methods.forceRefreshSelectedValue.call(this)
    },
  },
}
</script>
