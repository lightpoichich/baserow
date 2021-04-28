<template>
  <div class="crudtable">
    <header class="crudtable__header">
      <slot name="header"></slot>
      <CrudTableSearch :loading="loading" @search-changed="doSearch" />
    </header>
    <div
      :class="{ crudtable__loading: loading }"
      class="crudtable__rows"
      :style="{
        'grid-template-columns': columnWidths,
      }"
    >
      <template v-for="col in columns">
        <div
          :key="col.key"
          class="crudtable__field"
          :class="{
            'crudtable__field--sticky': col.isInLeftSection,
            'crudtable__field--right': col.hasRightBar,
            'crudtable__field--sortable': col.sortable,
          }"
          @click="toggleSort(col)"
        >
          {{ col.header }}
          <i
            v-if="sorted(col)"
            class="crudtable__field-icon fas"
            :class="sortIcon(col)"
          ></i>
        </div>
      </template>
      <template v-for="row in rows">
        <template v-for="col in columns">
          <component
            :is="col.cellComponent"
            :key="col.key + '-' + row.id"
            :row="row"
            :column="col"
            class="crudtable__cell"
            :class="{
              'crudtable__cell--sticky': col.isInLeftSection,
              'crudtable__cell--right': col.hasRightBar,
            }"
            @row-update="onRowUpdate"
            @row-delete="onRowDelete"
            @clicked="onClick"
          />
        </template>
      </template>
    </div>
    <div class="crudtable__footer">
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
      columnSorts: [],
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
    onClick(e) {
      console.log(e)
    },
    toggleSort(column) {
      if (!column.sortable) {
        return
      }
      const i = this.columnSorts.findIndex((c) => c.key === column.key)
      if (i === -1) {
        this.columnSorts.push({ key: column.key, direction: 'desc' })
      } else {
        const current = this.columnSorts[i]
        if (current.direction === 'desc') {
          this.columnSorts.splice(i, 1, {
            key: current.key,
            direction: 'asc',
          })
        } else {
          this.columnSorts.splice(i, 1)
        }
      }
      this.fetchPage(this.page)
    },
    sortIcon(column) {
      const i = this.columnSorts.findIndex((c) => c.key === column.key)
      return this.columnSorts[i].direction === 'desc'
        ? 'fa-sort-down'
        : 'fa-sort-up'
    },
    sorted(column) {
      return this.columnSorts.find((c) => c.key === column.key) !== undefined
    },
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
        const { data } = await this.service.fetchPage(
          page,
          searchQuery,
          this.columnSorts
        )
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
