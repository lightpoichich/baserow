<template>
  <Context ref="context" class="group-bys" max-height-if-outside-viewport>
    <div class="group-bys__content">
      <div
        v-if="view.group_bys.length === 0"
        v-auto-overflow-scroll
        class="group-bys__none group-bys__none--scrollable"
      >
        <div class="group-bys__none-title">
          {{ $t('viewGroupByContext.noGroupByTitle') }}
        </div>
        <div class="group-bys__none-description">
          {{ $t('viewGroupByContext.noGroupByText') }}
        </div>
      </div>

      <div
        v-if="view.group_bys.length > 0"
        v-auto-overflow-scroll
        class="group-bys__items group-bys__items--scrollable"
      >
        <div
          v-for="(groupBy, index) in view.group_bys"
          :key="groupBy.id"
          class="group-bys__item"
          :class="{
            'group-bys__item--loading': groupBy._.loading,
          }"
          :set="(field = getField(groupBy.field))"
        >
          <a
            v-if="!disableGroupBy"
            class="group-bys__remove"
            @click.stop="deleteGroupBy(groupBy)"
          >
            <i class="iconoir-cancel"></i>
          </a>
          <div class="group-bys__description">
            <template v-if="index === 0">{{
              $t('viewGroupByContext.groupBy')
            }}</template>
            <template v-if="index > 0">{{
              $t('viewGroupByContext.thenBy')
            }}</template>
          </div>
          <div class="group-bys__field">
            <Dropdown
              :value="groupBy.field"
              :disabled="disableGroupBy"
              :fixed-items="true"
              class="dropdown--floating"
              @input="updateGroupBy(groupBy, { field: $event })"
            >
              <DropdownItem
                v-for="field in fields"
                :key="'groupBy-field-' + groupBy.id + '-' + field.id"
                :name="field.name"
                :value="field.id"
                :disabled="
                  groupBy.field !== field.id && !isFieldAvailable(field)
                "
              >
              </DropdownItem>
            </Dropdown>
          </div>
          <div
            class="group-bys__order"
            :class="{ 'group-bys__order--disabled': disableGroupBy }"
          >
            <a
              class="group-bys__order-item"
              :class="{ active: groupBy.order === 'ASC' }"
              @click="updateGroupBy(groupBy, { order: 'ASC' })"
            >
              <template v-if="getGroupByIndicator(field, 0) === 'text'">{{
                getGroupByIndicator(field, 1)
              }}</template>
              <i
                v-if="getGroupByIndicator(field, 0) === 'icon'"
                :class="getGroupByIndicator(field, 1)"
              ></i>

              <i class="iconoir-arrow-right"></i>

              <template v-if="getGroupByIndicator(field, 0) === 'text'">{{
                getGroupByIndicator(field, 2)
              }}</template>
              <i
                v-if="getGroupByIndicator(field, 0) === 'icon'"
                class="fa"
                :class="getGroupByIndicator(field, 2)"
              ></i>
            </a>
            <a
              class="group-bys__order-item"
              :class="{ active: groupBy.order === 'DESC' }"
              @click="updateGroupBy(groupBy, { order: 'DESC' })"
            >
              <template v-if="getGroupByIndicator(field, 0) === 'text'">{{
                getGroupByIndicator(field, 2)
              }}</template>
              <i
                v-if="getGroupByIndicator(field, 0) === 'icon'"
                :class="getGroupByIndicator(field, 2)"
              ></i>

              <i class="iconoir-arrow-right"></i>

              <template v-if="getGroupByIndicator(field, 0) === 'text'">{{
                getGroupByIndicator(field, 1)
              }}</template>
              <i
                v-if="getGroupByIndicator(field, 0) === 'icon'"
                :class="getGroupByIndicator(field, 1)"
              ></i>
            </a>
          </div>
        </div>
      </div>
      <div
        v-if="view.group_bys.length < availableFieldsLength && !disableGroupBy"
        ref="addContextToggle"
        class="context__footer"
      >
        <ButtonText
          icon="iconoir-plus"
          @click="
            $refs.addContext.toggle($refs.addContextToggle, 'bottom', 'left', 4)
          "
        >
          {{ $t('viewGroupByContext.addGroupBy') }}</ButtonText
        >
        <Context
          ref="addContext"
          class="group-bys__add-context"
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
              <a class="context__menu-item-link" @click="addGroupBy(field)">
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
  name: 'ViewGroupByContext',
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
    disableGroupBy: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    /**
     * Calculates the total amount of available fields.
     */
    availableFieldsLength() {
      return this.fields.filter(this.getCanGroupByInView).length
    },
  },
  methods: {
    getCanGroupByInView(field) {
      return this.$registry.get('field', field.type).getCanGroupByInView(field)
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
      const allFieldIds = this.view.group_bys.map((groupBy) => groupBy.field)
      return this.getCanGroupByInView(field) && !allFieldIds.includes(field.id)
    },
    async addGroupBy(field) {
      this.$refs.addContext.hide()

      try {
        await this.$store.dispatch('view/createGroupBy', {
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
    async deleteGroupBy(groupBy) {
      try {
        await this.$store.dispatch('view/deleteGroupBy', {
          view: this.view,
          groupBy,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateGroupBy(groupBy, values) {
      if (this.disableGroupBy) {
        return
      }

      try {
        await this.$store.dispatch('view/updateGroupBy', {
          groupBy,
          values,
          readOnly: this.readOnly,
        })
        this.$emit('changed')
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    getGroupByIndicator(field, index) {
      return this.$registry
        .get('field', field.type)
        .getGroupByIndicator(field, this.$registry)[index]
    },
  },
}
</script>
