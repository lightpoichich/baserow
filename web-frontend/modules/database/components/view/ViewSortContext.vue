<template>
  <Context ref="context" class="sortings" max-height-if-outside-viewport>
    <div class="sortings__content">
      <div
        v-if="view.sortings.length === 0"
        v-auto-overflow-scroll
        class="sortings__none sortings__none--scrollable"
      >
        <div class="sortings__none-title">
          {{ $t('viewSortContext.noSortTitle') }}
        </div>
        <div class="sortings__none-description">
          {{ $t('viewSortContext.noSortText') }}
        </div>
      </div>
      <div
        v-if="view.sortings.length > 0"
        v-auto-overflow-scroll
        class="sortings__items sortings__items--scrollable"
      >
        <div
          v-for="(sort, index) in view.sortings"
          :key="sort.id"
          class="sortings__item"
          :class="{
            'sortings__item--loading': sort._.loading,
          }"
          :set="(field = getField(sort.field))"
        >
          <a
            v-if="!disableSort"
            class="sortings__remove"
            @click.stop="deleteSort(sort)"
          >
            <i class="iconoir-cancel"></i>
          </a>

          <div class="sortings__description">
            <template v-if="index === 0">{{
              $t('viewSortContext.sortBy')
            }}</template>
            <template v-if="index > 0">{{
              $t('viewSortContext.thenBy')
            }}</template>
          </div>
          <div class="sortings__field">
            <Dropdown
              :value="sort.field"
              :disabled="disableSort"
              :fixed-items="true"
              class="dropdown--floating"
              @input="updateSort(sort, { field: $event })"
            >
              <DropdownItem
                v-for="field in fields"
                :key="'sort-field-' + sort.id + '-' + field.id"
                :name="field.name"
                :value="field.id"
                :disabled="sort.field !== field.id && !isFieldAvailable(field)"
              ></DropdownItem>
            </Dropdown>
          </div>
          <div
            class="sortings__order"
            :class="{ 'sortings__order--disabled': disableSort }"
          >
            <a
              class="sortings__order-item"
              :class="{ active: sort.order === 'ASC' }"
              @click="updateSort(sort, { order: 'ASC' })"
            >
              <template v-if="getSortIndicator(field, 0) === 'text'">{{
                getSortIndicator(field, 1)
              }}</template>
              <i
                v-if="getSortIndicator(field, 0) === 'icon'"
                :class="getSortIndicator(field, 1)"
              ></i>

              <i class="iconoir-arrow-right"></i>

              <template v-if="getSortIndicator(field, 0) === 'text'">{{
                getSortIndicator(field, 2)
              }}</template>
              <i
                v-if="getSortIndicator(field, 0) === 'icon'"
                :class="getSortIndicator(field, 2)"
              ></i>
            </a>
            <a
              class="sortings__order-item"
              :class="{ active: sort.order === 'DESC' }"
              @click="updateSort(sort, { order: 'DESC' })"
            >
              <template v-if="getSortIndicator(field, 0) === 'text'">{{
                getSortIndicator(field, 2)
              }}</template>
              <i
                v-if="getSortIndicator(field, 0) === 'icon'"
                :class="getSortIndicator(field, 2)"
              ></i>

              <i class="iconoir-arrow-right"></i>

              <template v-if="getSortIndicator(field, 0) === 'text'">{{
                getSortIndicator(field, 1)
              }}</template>
              <i
                v-if="getSortIndicator(field, 0) === 'icon'"
                :class="getSortIndicator(field, 1)"
              ></i>
            </a>
          </div>
        </div>
      </div>
      <div
        v-if="view.sortings.length < availableFieldsLength && !disableSort"
        ref="addContextToggle"
        class="context__footer"
      >
        <ButtonText
          icon="iconoir-plus"
          @click="
            $refs.addContext.toggle($refs.addContextToggle, 'bottom', 'left', 4)
          "
        >
          {{ $t('viewSortContext.addSort') }}</ButtonText
        >
        <Context
          ref="addContext"
          class="sortings__add-context"
          overflow-scroll
          max-height-if-outside-viewport
        >
          <ul ref="items" class="context__menu">
            <li
              v-for="field in fields"
              v-show="isFieldAvailable(field)"
              :key="field.id"
              class="context__menu-item"
            >
              <a class="context__menu-item-link" @click="addSort(field)">
                <i
                  class="context__menu-item-icon"
                  :class="field._.type.iconClass"
                ></i>
                {{ field.name }}
              </a>
            </li>
          </ul>
        </Context>
      </div>
    </div>
  </Context>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import context from '@baserow/modules/core/mixins/context'

export default {
  name: 'ViewSortContext',
  mixins: [context],
  props: {
    fields: {
      type: Array,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
    disableSort: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    /**
     * Calculates the total amount of available fields.
     */
    availableFieldsLength() {
      return this.fields.filter(this.getCanSortInView).length
    },
  },
  methods: {
    getCanSortInView(field) {
      return this.$registry.get('field', field.type).getCanSortInView(field)
    },
    getField(fieldId) {
      for (const i in this.fields) {
        if (this.fields[i].id === fieldId) {
          return this.fields[i]
        }
      }
      return undefined
    },
    isFieldAvailable(field) {
      const allFieldIds = this.view.sortings.map((sort) => sort.field)
      return this.getCanSortInView(field) && !allFieldIds.includes(field.id)
    },
    async addSort(field) {
      this.$refs.addContext.hide()

      try {
        await this.$store.dispatch('view/createSort', {
          view: this.view,
          values: {
            field: field.id,
            value: 'ASC',
          },
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async deleteSort(sort) {
      try {
        await this.$store.dispatch('view/deleteSort', {
          view: this.view,
          sort,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateSort(sort, values) {
      if (this.disableSort) {
        return
      }

      try {
        await this.$store.dispatch('view/updateSort', {
          sort,
          values,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    getSortIndicator(field, index) {
      return this.$registry
        .get('field', field.type)
        .getSortIndicator(field, this.$registry)[index]
    },
  },
}
</script>
