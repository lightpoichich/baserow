export const addVuex = (context) => {
  context.vuex = require('vuex')
  context.vue.use(context.vuex)
}
export const addFilter = (name, lambda) => {
  return (context) => context.vue.filter(name, lambda)
}
export const compositeConfiguration = (...configs) => {
  return (context) => configs.forEach((config) => config(context))
}
export const bootstrapVueContext = (configureContext) => {
  configureContext = configureContext || compositeConfiguration(addVuex)
  const context = {}
  const teardownVueContext = () => {
    jest.unmock('vue')
    Object.keys(context).forEach((key) => delete context[key])
    jest.resetModules()
  }

  jest.isolateModules(() => {
    context.vueTestUtils = require('@vue/test-utils')
    context.vue = context.vueTestUtils.createLocalVue()

    jest.doMock('vue', () => context.vue)

    configureContext && configureContext(context)
  })

  return {
    teardownVueContext,
    ...context,
  }
}
