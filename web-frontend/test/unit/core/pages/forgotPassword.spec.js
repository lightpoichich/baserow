import { TestApp } from '@baserow/test/helpers/testApp'
import forgotPasswordPage from '@baserow/modules/core/pages/forgotPassword'

class ForgotPasswordPageHelpers {
  constructor(forgotPasswordPageComponent) {
    this.c = forgotPasswordPageComponent
  }

  findForm() {
    return this.c.find('form')
  }

  findEmailInput() {
    return this.c.find('form input')
  }

  errorEmailRequired() {
    return this.c.vm.v$.email.required.$invalid
  }

  errorEmailInvalid() {
    return this.c.vm.v$.email.email.$invalid
  }

  async setEmailInputValue(value) {
    await this.findEmailInput().setValue(value)
    await this.findEmailInput().trigger('input')
    await this.forceUpdate()
  }

  async triggerEmailInputBlur() {
    await this.findEmailInput().trigger('blur')
    await this.c.vm.v$.$touch()
    await this.forceUpdate()
  }

  async triggerSubmit() {
    await this.findForm().trigger('submit.prevent')
    await this.forceUpdate()
  }

  isInvalidEmailErrorMessageShown() {
    return this.c.html().includes('error.invalidEmail')
  }

  async forceUpdate() {
    await this.c.vm.$nextTick()
    await this.c.vm.$forceUpdate()
  }
}

describe('forgotPassword page', () => {
  let testApp = null

  beforeEach(() => {
    testApp = new TestApp()
  })

  afterEach(() => testApp.afterEach())

  async function whenTheForgotPasswordFormIsShown() {
    testApp.store.commit('settings/SET_SETTINGS', {
      allow_reset_password: true,
    })
    const page = await testApp.mount(forgotPasswordPage, { sync: false })
    const helper = new ForgotPasswordPageHelpers(page)
    return { page, helper }
  }

  test('Default form match snapshot', async () => {
    const { page } = await whenTheForgotPasswordFormIsShown()
    expect(page.element).toMatchSnapshot()
  })

  test('A form is rendered', async () => {
    const { helper } = await whenTheForgotPasswordFormIsShown()
    // Ensure the form exists
    expect(helper.findForm().exists()).toBe(true)
  })

  test('An error is shown if the email is empty', async () => {
    const { helper } = await whenTheForgotPasswordFormIsShown()

    expect(helper.isInvalidEmailErrorMessageShown()).toBe(false)

    await helper.triggerSubmit()

    expect(helper.errorEmailRequired()).toBe(true)
    expect(helper.errorEmailInvalid()).toBe(false)
    expect(helper.isInvalidEmailErrorMessageShown()).toBe(true)
  })

  test('An error is shown if the email is not valid', async () => {
    const { helper } = await whenTheForgotPasswordFormIsShown()

    expect(helper.isInvalidEmailErrorMessageShown()).toBe(false)

    await helper.setEmailInputValue('invalid-email')
    await helper.triggerEmailInputBlur()

    expect(helper.errorEmailRequired()).toBe(false)
    expect(helper.errorEmailInvalid()).toBe(true)
    expect(helper.isInvalidEmailErrorMessageShown()).toBe(true)
  })

  test('No error is shown with a valid email', async () => {
    const { helper } = await whenTheForgotPasswordFormIsShown()

    await helper.setEmailInputValue('valid@email.com')
    await helper.triggerEmailInputBlur()

    expect(helper.errorEmailRequired()).toBe(false)
    expect(helper.errorEmailInvalid()).toBe(false)
    expect(helper.isInvalidEmailErrorMessageShown()).toBe(false)
  })
})
