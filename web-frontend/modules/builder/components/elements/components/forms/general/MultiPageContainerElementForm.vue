<template>
  <form @submit.prevent @keydown.enter.prevent>
    <FormGroup
      small-label
      :label="$t('multiPageContainerElementForm.pagePosition')"
      class="margin-bottom-2"
      required
    >
      <Dropdown v-model="values.page_position" :show-search="false" small>
        <DropdownItem
          v-for="pos in pagePositions"
          :key="pos.value"
          :name="pos.label"
          :value="pos.value"
        >
          {{ pos.label }}
        </DropdownItem>
      </Dropdown>
    </FormGroup>
    <FormGroup
      small-label
      :label="$t('multiPageContainerElementForm.display')"
      class="margin-bottom-2"
      required
    >
      <Dropdown v-model="values.share_type" :show-search="false" small>
        <DropdownItem
          v-for="item in pageShareTypes"
          :key="item.value"
          :name="item.label"
          :value="item.value"
        >
          {{ item.label }}
        </DropdownItem>
      </Dropdown>
    </FormGroup>
  </form>
</template>

<script>
import elementForm from '@baserow/modules/builder/mixins/elementForm'
import { PAGE_POSITIONS, SHARE_TYPES } from '@baserow/modules/builder/enums'

export default {
  name: 'MultiPageContainerElementForm',
  mixins: [elementForm],
  data() {
    return {
      values: {
        page_position: '',
        share_type: '',
        pages: [],
        styles: {},
      },
      allowedValues: ['page_position', 'share_type', 'pages', 'styles'],
    }
  },
  computed: {
    pagePositions() {
      return [
        {
          label: this.$t('pagePosition.header'),
          value: PAGE_POSITIONS.HEADER,
        },
        {
          label: this.$t('pagePosition.footer'),
          value: PAGE_POSITIONS.FOOTER,
        },
      ]
    },
    pageShareTypes() {
      return [
        {
          label: this.$t('pageShareType.all'),
          value: SHARE_TYPES.ALL,
        },
        {
          label: this.$t('pageShareType.only'),
          value: SHARE_TYPES.ONLY,
        },
        {
          label: this.$t('pageShareType.except'),
          value: SHARE_TYPES.EXCEPT,
        },
      ]
    },
  },
}
</script>
