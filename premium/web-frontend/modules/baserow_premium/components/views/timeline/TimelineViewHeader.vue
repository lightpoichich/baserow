<template>
  <ul v-if="!tableLoading" class="header__filter header__filter--full-width">
    <li class="header__filter-item">
      <a
        ref="dateSettingsLink"
        class="header__filter-link"
        :class="!canChooseDatesField ? 'header__filter-link--disabled' : ''"
        @click="showChooseDatesFieldContext"
      >
        <i class="header__filter-icon iconoir-calendar"></i>
        <span class="header__filter-name">
          {{ $t('timelineViewHeader.dateSettings') }}
        </span>
      </a>
      <SelectDatesFieldContext
        ref="dateSettingsContext"
        :fields="fields"
        :view="view"
        @refresh="$emit('refresh', $event)"
      >
      </SelectDatesFieldContext>
    </li>
    <li v-if="startDateFieldId != null" class="header__filter-item">
      <a
        ref="customizeContextLink"
        class="header__filter-link"
        @click="
          $refs.customizeContext.toggle(
            $refs.customizeContextLink,
            'bottom',
            'left',
            4
          )
        "
      >
        <i class="header__filter-icon iconoir-list"></i>
        <span class="header__filter-name">{{
          $t('timelineViewHeader.labels')
        }}</span>
      </a>
      <ViewFieldsContext
        ref="customizeContext"
        :database="database"
        :view="view"
        :fields="fields"
        :field-options="fieldOptions"
        :allow-cover-image-field="false"
        @update-all-field-options="updateAllFieldOptions"
        @update-field-options-of-field="updateFieldOptionsOfField"
        @update-order="orderFieldOptions"
      ></ViewFieldsContext>
    </li>
    <li v-if="isDev" class="header__filter-item">
      <div>
        <Badge color="yellow" indicator>Debug</Badge>
        <span>{{ timezone }}</span>
      </div>
    </li>
    <li class="header__filter-item header__filter-item--right">
      <ViewSearch
        :view="view"
        :fields="fields"
        :store-prefix="storePrefix"
        :always-hide-rows-not-matching-search="true"
        @refresh="$emit('refresh', $event)"
      ></ViewSearch>
    </li>
  </ul>
</template>

<script>
import { mapState, mapGetters } from 'vuex'

import { notifyIf } from '@baserow/modules/core/utils/error'
import SelectDatesFieldContext from '@baserow_premium/components/views/timeline/SelectDatesFieldContext'
import ViewFieldsContext from '@baserow/modules/database/components/view/ViewFieldsContext'
import ViewSearch from '@baserow/modules/database/components/view/ViewSearch'
import { getUserTimeZone } from '@baserow/modules/core/utils/date'

export default {
  name: 'TimelineViewHeader',
  components: {
    ViewFieldsContext,
    SelectDatesFieldContext,
    ViewSearch,
  },
  props: {
    storePrefix: {
      type: String,
      required: true,
      default: '',
    },
    database: {
      type: Object,
      required: true,
    },
    table: {
      type: Object,
      required: true,
    },
    view: {
      type: Object,
      required: true,
    },
    fields: {
      type: Array,
      required: true,
    },
    readOnly: {
      type: Boolean,
      required: true,
    },
  },
  computed: {
    startDateFieldId() {
      return this.view.start_date_field
    },
    startDateField() {
      return this.getStartDateField()
    },
    timezone() {
      const dateField = this.startDateField
      let timezone
      if (dateField?.date_include_time) {
        timezone = dateField.date_force_timezone
      } else {
        timezone = getUserTimeZone()
      }
      return timezone
    },
    displayedByFieldName() {
      for (let i = 0; i < this.fields.length; i++) {
        if (this.fields[i].id === this.view.date_field) {
          return this.fields[i].name
        }
      }
      return ''
    },
    isDev() {
      return process.env.NODE_ENV === 'development'
    },
    ...mapState({
      tableLoading: (state) => state.table.loading,
    }),
    canChooseDatesField() {
      return (
        !this.readOnly &&
        this.$hasPermission(
          'database.table.view.update',
          this.view,
          this.database.workspace.id
        )
      )
    },
  },
  beforeCreate() {
    this.$options.computed = {
      ...(this.$options.computed || {}),
      ...mapGetters({
        fieldOptions:
          this.$options.propsData.storePrefix +
          'view/timeline/getAllFieldOptions',
      }),
    }
  },
  methods: {
    getStartDateField() {
      return this.fields.find(
        (field) => field.id === this.view.start_date_field
      )
    },
    showChooseDatesFieldContext() {
      if (this.canChooseDatesField) {
        this.$refs.dateSettingsContext.toggle(
            this.$refs.dateSettingsLink,
            'bottom',
            'left',
            4
          )
      }
    },
    async updateAllFieldOptions({ newFieldOptions, oldFieldOptions }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/timeline/updateAllFieldOptions',
          {
            newFieldOptions,
            oldFieldOptions,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.workspace.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async updateFieldOptionsOfField({ field, values, oldValues }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/timeline/updateFieldOptionsOfField',
          {
            field,
            values,
            oldValues,
            readOnly:
              this.readOnly ||
              !this.$hasPermission(
                'database.table.view.update_field_options',
                this.view,
                this.database.workspace.id
              ),
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
    async orderFieldOptions({ order }) {
      try {
        await this.$store.dispatch(
          this.storePrefix + 'view/timeline/updateFieldOptionsOrder',
          {
            order,
            readOnly: this.readOnly,
          }
        )
      } catch (error) {
        notifyIf(error, 'view')
      }
    },
  },
}
</script>
