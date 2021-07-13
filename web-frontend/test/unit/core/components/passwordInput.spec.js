import PasswordInput from '@baserow/modules/core/components/helpers/PasswordInput'
import { bootstrapVueContext } from '@baserow/test/helpers/components'

describe('Password Input Tests', () => {
  let vueContext = null

  beforeEach(() => {
    vueContext = bootstrapVueContext()
  })

  afterEach(() => {
    vueContext.teardownVueContext()
  })

  function mountPasswordInput(passwordValue) {
    return vueContext.vueTestUtils.mount(PasswordInput, {
      localVue: vueContext.vue,
      propsData: {
        label: 'Password',
        name: 'password',
        passwordValue,
      },
    })
  }

  function getErrorDiv(wrapper) {
    return wrapper.find('div > .error')
  }

  function getErrorText(errorDiv) {
    return errorDiv.text().replace(/\n/gm, '').replace(/\s\s+/g, ' ')
  }

  test('Correct password does not render error div', async () => {
    const wrapper = mountPasswordInput('thisIsAValidPassword')
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    expect(errorDiv.exists()).toBeFalsy()
    expect(inputInvalid).toBeFalsy()
  })

  test('Password must be minimum of 8 characters', async () => {
    const wrapper = mountPasswordInput('short')
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    const errorText = getErrorText(errorDiv)
    expect(errorText).toBe('A minimum of 8 characters is required here.')
    expect(inputInvalid).toBeTruthy()
  })

  test('Password cannot be empty', async () => {
    const wrapper = mountPasswordInput('')
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    const errorText = getErrorText(errorDiv)
    expect(errorText).toBe('Input is required.')
    expect(inputInvalid).toBeTruthy()
  })

  test('Password cannot be more than 256 characters', async () => {
    const longPassword = 't'.repeat(257)
    const wrapper = mountPasswordInput(longPassword)
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    const errorText = getErrorText(errorDiv)
    expect(errorText).toBe('A maximum of 256 characters is allowed here.')
    expect(inputInvalid).toBeTruthy()
  })

  test('Password can be exactly 256 characters', async () => {
    const longPassword = 't'.repeat(256)
    const wrapper = mountPasswordInput(longPassword)
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    expect(errorDiv.exists()).toBeFalsy()
    expect(inputInvalid).toBeFalsy()
  })

  test('Password can be exactly 8 characters', async () => {
    const longPassword = 't'.repeat(8)
    const wrapper = mountPasswordInput(longPassword)
    await wrapper.vm.$v.passwordValue.$touch()
    const inputInvalid = wrapper.vm.$v.$invalid
    const errorDiv = getErrorDiv(wrapper)
    expect(errorDiv.exists()).toBeFalsy()
    expect(inputInvalid).toBeFalsy()
  })
})
