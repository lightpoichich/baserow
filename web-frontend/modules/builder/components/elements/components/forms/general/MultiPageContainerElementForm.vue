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
      :label="$t('multiPageContainerElementForm.behaviour')"
      class="margin-bottom-2"
      required
    >
      <Dropdown v-model="values.behaviour" :show-search="false" small>
        <DropdownItem
          v-for="item in scrollBehaviours"
          :key="item.value"
          :name="item.label"
          :value="item.value"
        >
          {{ item.label }}
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
import {
  PAGE_POSITIONS,
  SCROLL_BEHAVIOURS,
  SHARE_TYPES,
} from '@baserow/modules/builder/enums'

export default {
  name: 'MultiPageContainerElementForm',
  mixins: [elementForm],
  data() {
    return {
      values: {
        page_position: '',
        behaviour: '',
        share_type: '',
        pages: [],
        styles: {},
      },
      allowedValues: [
        'page_position',
        'behaviour',
        'share_type',
        'pages',
        'styles',
      ],
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
        {
          label: this.$t('pagePosition.left'),
          value: PAGE_POSITIONS.LEFT,
        },
        {
          label: this.$t('pagePosition.right'),
          value: PAGE_POSITIONS.RIGHT,
        },
      ]
    },
    scrollBehaviours() {
      return [
        {
          label: this.$t('scrollBehaviour.scroll'),
          value: SCROLL_BEHAVIOURS.SCROLL,
        },
        {
          label: this.$t('scrollBehaviour.fixed'),
          value: SCROLL_BEHAVIOURS.FIXED,
        },
        {
          label: this.$t('scrollBehaviour.sticky'),
          value: SCROLL_BEHAVIOURS.STICKY,
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
