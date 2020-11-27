<template>
  <Context ref="context" class="hidings">
    <div>
      <ul class="context__menu">
        <li v-for="field in fields" :key="field.id" class="hidings__item">
          <SwitchInput
            :value="field.hidden"
            @input="updateFieldOptionsOfField(field, { hidden: $event })"
          />
          <i class="fas" :class="'fa-' + field._.type.iconClass"></i>
          <span>{{ field.name }}</span>
        </li>
      </ul>
    </div>
    <div class="hidings__footer">
      <button class="button button--ghost">Hide all</button>
      <button class="button button--ghost">Show all</button>
    </div>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import { notifyIf } from '@/modules/core/utils/error'

export default {
  name: 'ViewHideContext',
  mixins: [context],
  props: {
    primary: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
  },
  methods: {
    async updateFieldOptionsOfField(field, values) {
      console.log(this.view)
      try {
        await this.$store.dispatch('view/grid/updateFieldOptionsOfField', {
          gridId: this.view.id,
          field,
          values,
          oldValues: {
            hidden: field.hidden,
          },
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
}
</script>
