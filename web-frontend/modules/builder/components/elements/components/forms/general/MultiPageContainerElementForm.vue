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
      <template v-if="values.share_type !== 'all'">
        <div class="multi-page-container-element-form__page-list">
          <div
            v-for="page in pages"
            :key="page.id"
            class="multi-page-container-element-form__page-checkbox"
          >
            <Checkbox
              :checked="values.pages.includes(page.id)"
              @input="togglePage(page)"
            >
              {{ page.name }}
            </Checkbox>
          </div>

          <div class="multi-page-container-element-form__actions">
            <a @click.prevent="selectAll">
              {{ $t('multiPageContainerElementForm.selectAll') }}
            </a>
            <a
              class="multi-page-container-element-form__deselect-all"
              @click.prevent="deselectAll"
            >
              {{ $t('multiPageContainerElementForm.deselectAll') }}
            </a>
          </div>
        </div>
      </template>
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
    pages() {
      return this.$store.getters['page/getVisiblePages'](this.builder)
    },
  },
  methods: {
    togglePage(page) {
      if (!this.values.pages.includes(page.id)) {
        this.values.pages.push(page.id)
      } else {
        this.values.pages = this.values.pages.filter(
          (pageId) => pageId !== page.id
        )
      }
    },
    selectAll() {
      this.values.pages = this.pages.map(({ id }) => id)
    },
    deselectAll() {
      this.values.pages = []
    },
  },
}
</script>
