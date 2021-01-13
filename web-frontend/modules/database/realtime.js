/**
 * Registers the real time events related to the database module.
 */
export const registerRealtimeEvents = (realtime) => {
  realtime.registerEvent('table_created', ({ store }, data) => {
    const database = store.getters['application/get'](data.table.database_id)
    if (database !== undefined) {
      store.dispatch('table/forceCreate', { database, data: data.table })
    }
  })

  realtime.registerEvent('table_updated', ({ store }, data) => {
    const database = store.getters['application/get'](data.table.database_id)
    if (database !== undefined) {
      const table = database.tables.find((table) => table.id === data.table.id)
      if (table !== undefined) {
        store.dispatch('table/forceUpdate', {
          database,
          table,
          values: data.table,
        })
      }
    }
  })

  realtime.registerEvent('table_deleted', ({ store }, data) => {
    const database = store.getters['application/get'](data.database_id)
    if (database !== undefined) {
      const table = database.tables.find((table) => table.id === data.table_id)
      if (table !== undefined) {
        store.dispatch('table/forceDelete', { database, table })
      }
    }
  })
}
