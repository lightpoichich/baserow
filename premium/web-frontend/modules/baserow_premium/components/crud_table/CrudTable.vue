<template>
  <div class="crud-table-wrapper">
    <header class="crud_header">
      <slot name="header"></slot>
      <CrudTableSearch :loading="loading" @search-changed="doSearch" />
    </header>
    <div
      :class="{ 'crud-table-rows__loading': loading }"
      class="crud-table-rows"
      :style="{
        'grid-template-columns': columnWidths,
      }"
    >
      <template v-for="col in columns">
        <div
          :key="col.key"
          class="crud-table-rows__field"
          :class="{
            'crud-table-rows__field-sticky': col.isInLeftSection,
            'crud-table-rows__field-right': col.hasRightBar,
          }"
        >
          {{ col.header }}
          <i v-if="col.icon" class="fas" :class="col.icon"></i>
        </div>
      </template>
      <template v-for="row in rows">
        <template v-for="col in columns">
          <div
            :key="col.key + '-' + row.id"
            class="crud-table-rows__cell"
            :class="{
              'crud-table-rows__cell-sticky': col.isInLeftSection,
              'crud-table-rows__cell-right': col.hasRightBar,
            }"
          >
            <component
              :is="col.cellComponent"
              :row="row"
              :column="col"
              @row-update="onRowUpdate"
              @row-delete="onRowDelete"
            />
          </div>
        </template>
      </template>
    </div>
    <div class="crud-table-rows__foot">
      <Paginator
        :page="page"
        :total-pages="totalPages"
        @change-page="fetchPage"
      ></Paginator>
    </div>
  </div>
</template>

<script>
import { notifyIf } from '@baserow/modules/core/utils/error'
import CrudTableSearch from '@baserow_premium/components/crud_table/CrudTableSearch'
import Paginator from '@baserow/modules/core/components/Paginator'

export default {
  name: 'CrudTable',
  components: { Paginator, CrudTableSearch },
  props: {
    service: {
      required: true,
      type: Object,
    },
    columns: {
      required: true,
      type: Array,
    },
  },
  data() {
    return {
      loading: false,
      page: 1,
      totalPages: null,
      rows: [],
    }
  },
  async fetch() {
    await this.fetchPage(1, {})
  },
  computed: {
    columnWidths() {
      return this.columns
        .map((c) => `minmax(${c.minWidth}, ${c.maxWidth})`)
        .join(' ')
    },
  },
  methods: {
    async doSearch(searchQuery) {
      this.totalPages = null
      await this.fetchPage(1, { searchQuery })
    },
    /**
     * Fetches the rows of a given page and adds them to the state. If a search query
     * has been stored in the state then that will be remembered.
     */
    async fetchPage(page, { searchQuery = '' } = {}) {
      this.loading = true

      try {
        const { data } = await this.service.fetchPage(page, searchQuery)
        this.page = page
        this.totalPages = Math.ceil(data.count / 100)
        this.rows = data.results
      } catch (error) {
        notifyIf(error, 'row')
      }

      this.loading = false
    },
    onRowUpdate(updatedRow) {
      const i = this.rows.findIndex((u) => u.id === updatedRow.id)
      this.rows.splice(i, 1, updatedRow)
    },
    onRowDelete(rowId) {
      const i = this.rows.findIndex((u) => u.id === rowId)
      this.rows.splice(i, 1)
    },
  },
}
</script>
