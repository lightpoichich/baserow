import setupCore from '@baserow/modules/core/plugin'
import axios from 'axios'
import setupDatabasePlugin from '@baserow/modules/database/plugin'
import { bootstrapVueContext } from '@baserow/test/helpers/components'
import MockAdapter from 'axios-mock-adapter'
import _ from 'lodash'
import { MockServer } from '@baserow/test/fixtures/mockServer'
import flushPromises from 'flush-promises'

function createBaserowStore(app, vueContext) {
  const store = new vueContext.vuex.Store({})
  setupCore({ store, app }, (name, dep) => {
    app[`$${name}`] = dep
  })
  store.$registry = app.$registry
  store.$client = axios
  store.app = app
  app.$store = store
  setupDatabasePlugin({
    store,
    app,
  })
  return store
}

export class TestApp {
  constructor() {
    this.realtime = {
      registerEvent(e, f) {},
      subscribe(e, f) {},
    }
    this.app = {
      $realtime: this.realtime,
      $cookies: {
        set(name, id, value) {},
      },
      $env: {
        PUBLIC_WEB_FRONTEND_URL: 'https://localhost/',
      },
    }
    this.mock = new MockAdapter(axios)
    this.vueContext = bootstrapVueContext()
    this.store = createBaserowStore(this.app, this.vueContext)
    this.initialCleanStoreState = _.cloneDeep(this.store.state)
    this.mockServer = new MockServer(this.mock, this.store)
  }

  afterEach() {
    this.mock.reset()
    this.store.replaceState(_.cloneDeep(this.initialCleanStoreState))
    this.vueContext.teardownVueContext()
  }

  async mount(Component, { asyncDataParams = {} }) {
    if (Object.prototype.hasOwnProperty.call(Component, 'asyncData')) {
      const data = await Component.asyncData({
        store: this.store,
        params: asyncDataParams,
        error: fail,
        app: this.app,
      })
      Component.data = function () {
        return data
      }
    }
    return this.vueContext.vueTestUtils.mount(Component, {
      localVue: this.vueContext.vue,
      mocks: this.app,
    })
  }

  async performSearch(tableComponent, searchTerm) {
    const searchBox = tableComponent.get(
      'input[placeholder*="Search in all rows"]'
    )
    await searchBox.setValue(searchTerm)
    await searchBox.trigger('submit')
    await flushPromises()
  }

  async startEditForCellContaining(tableComponent, htmlInsideCellToSearchFor) {
    const targetCell = tableComponent
      .findAll('.grid-view__cell')
      .filter((w) => w.html().includes(htmlInsideCellToSearchFor))
      .at(0)

    await targetCell.trigger('click')

    const activeCell = tableComponent.get('.grid-view__cell.active')
    // Double click to start editing cell
    await activeCell.trigger('click')
    await activeCell.trigger('click')

    return activeCell.find('input')
  }
}
