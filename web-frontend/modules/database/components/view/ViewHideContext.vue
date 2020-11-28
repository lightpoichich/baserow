<template>
  <Context ref="context" class="hidings">
    <div>
      <ul class="context__menu">
        <li v-for="field in fields" :key="field.id" class="hidings__item">
          <SwitchInput
            :value="isFieldVisible(field)"
            @input="updateFieldOptionsOfField(field, { hidden: !$event })"
          />
          <i class="fas" :class="'fa-' + field._.type.iconClass"></i>
          <span>{{ field.name }}</span>
        </li>
      </ul>
    </div>
    <div class="hidings__footer">
      <button class="button button--ghost" @click="updateAll(true)">
        Hide all
      </button>
      <button class="button button--ghost" @click="updateAll(false)">
        Show all
      </button>
    </div>
  </Context>
</template>

<script>
import context from '@baserow/modules/core/mixins/context'
import { notifyIf } from '@/modules/core/utils/error'
import { mapGetters } from 'vuex'

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
  computed: {
    ...mapGetters({
      fieldOptions: 'view/grid/getAllFieldOptions',
    }),
  },
  methods: {
    updateAll(value) {
      this.fields.forEach((field) => {
        this.updateFieldOptionsOfField(field, { hidden: value })
      })
    },
    async updateFieldOptionsOfField(field, values) {
      try {
        await this.$store.dispatch('view/grid/updateFieldOptionsOfField', {
          gridId: this.view.id,
          field,
          values,
          oldValues: {
            hidden: this.isFieldVisible(field),
          },
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    isFieldVisible(field) {
      return !this.fieldOptions[field.id].hidden
    },
  },
}
</script>
