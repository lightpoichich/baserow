import { TestApp } from '@baserow/test/helpers/testApp'
import UsersAdminContent from '@baserow_premium/components/admin/user/UsersAdminContent'
import moment from 'moment'
import flushPromises from 'flush-promises'
import DeleteUserModal from '@baserow_premium/components/admin/user/DeleteUserModal'
import UserAdminUserHelpers from '../../../../fixtures/uiHelpers'
import MockPremiumServer from '@baserow_premium/../../test/fixtures/mockPremiumServer'

// Mock out debounce so we dont have to wait or simulate waiting for the various
// debounces in the search functionality.
jest.mock('lodash/debounce', () => jest.fn((fn) => fn))

describe('User Admin Component Tests', () => {
  let testApp = null
  let mockPremiumServer = null

  beforeAll(() => {
    testApp = new TestApp()
    mockPremiumServer = new MockPremiumServer(testApp.mock)
  })

  afterEach(() => testApp.afterEach())

  test('A users attributes will be displayed', async () => {
    const userSetup = {
      id: 1,
      username: 'user@baserow.io',
      fullName: 'user name',
      groups: [
        {
          id: 4,
          name: "users's group",
          permissions: 'ADMIN',
        },
        {
          id: 65,
          name: 'other_group',
        },
      ],
      lastLogin: '2021-04-26T07:50:45.643059Z',
      dateJoined: '2021-04-21T12:04:27.379781Z',
      isActive: true,
      isStaff: true,
    }
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin(userSetup)

    const cells = ui.findCells()
    expect(cells.length).toBe(7)
    const {
      userIdCell,
      usernameCell,
      fullNameCell,
      groupsCell,
      lastLoginCell,
      signedUpCell,
      isActiveCell,
    } = ui.getRow(cells, 0)

    expect(userIdCell.text()).toBe('1')

    // Username matches with correct initials and has an admin icon
    expect(usernameCell.text()).toContain(userSetup.username)
    expect(ui.usernameCellIsForStaffMember(usernameCell)).toBe(true)
    expect(ui.getUsernameInitials(usernameCell)).toBe('UN')

    // First name matches
    expect(fullNameCell.text()).toBe(userSetup.fullName)

    // Has two groups
    const groups = ui.getGroups(groupsCell)
    expect(groups.length).toBe(2)
    const firstGroup = groups.at(0)
    const secondGroup = groups.at(1)

    // The first group has the correct name and as the user is an admin an icon is
    // displayed
    expect(firstGroup.text()).toBe("users's group")
    expect(ui.groupCellShowsThisUserIsGroupAdmin(firstGroup)).toBe(true)

    // The second group has the right name and no admin icon as the user is not an
    // admin
    expect(secondGroup.text()).toBe('other_group')
    expect(ui.groupCellShowsThisUserIsGroupAdmin(secondGroup)).toBe(false)

    // The last login and signed up dates are correctly formatted to the locale
    moment.locale('nl')
    expect(lastLoginCell.text()).toBe('04/26/2021 7:50 AM')
    expect(signedUpCell.text()).toBe('04/21/2021 12:04 PM')

    // Shown as active
    expect(isActiveCell.text()).toBe('Active')
  })

  test('A user can be deleted', async () => {
    const { user, userAdmin, ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    expect(userAdmin.html()).toContain(user.username)

    const editUserContext = await ui.openFirstUserActionsMenu()
    await ui.clickDeleteUser(editUserContext)

    mockPremiumServer.expectUserDeleted(user.id)

    await userAdmin
      .findComponent(DeleteUserModal)
      .find('button')
      .trigger('click')

    await flushPromises()

    expect(userAdmin.html()).not.toContain(user.username)
  })

  test('An active user can be deactivated', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      isActive: true,
    })

    const editUserContext = await ui.openFirstUserActionsMenu()

    mockPremiumServer.expectUserUpdated(user, {
      is_active: false,
    })

    await ui.clickDeactivateUser(editUserContext)

    await flushPromises()

    const cells = ui.findCells()
    const { isActiveCell } = ui.getRow(cells, 0)
    expect(isActiveCell.text()).toContain('Deactivated')
  })

  test('A deactivated user can be activated', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      isActive: false,
    })

    const editUserContext = await ui.openFirstUserActionsMenu()

    mockPremiumServer.expectUserUpdated(user, {
      is_active: true,
    })

    await ui.clickActivateUser(editUserContext)

    await flushPromises()

    const cells = ui.findCells()
    const { isActiveCell } = ui.getRow(cells, 0)
    expect(isActiveCell.text()).toContain('Active')
  })

  test('A users password can be changed', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const newValidPassword = '12345678'
    mockPremiumServer.expectUserUpdated(user, {
      password: newValidPassword,
    })

    await ui.changePassword(newValidPassword, newValidPassword)

    await flushPromises()
  })

  test('users password cant be changed if not entered the same twice', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const validPassword = '1'.repeat(8)

    expect(
      await ui.attemptToChangePasswordReturningModalError(
        validPassword,
        validPassword + 'DifferentFromFirst'
      )
    ).toContain('This field must match your password field')
  })

  test('users password cant be changed less than 8 characters', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const tooShortPassword = '1'.repeat(7)

    expect(
      await ui.attemptToChangePasswordReturningModalError(
        tooShortPassword,
        tooShortPassword
      )
    ).toContain('A minimum of 8 characters is required here.')
  })

  test('users password cant be changed to more than 256 characters', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const tooLongPassword = '1'.repeat(257)

    expect(
      await ui.attemptToChangePasswordReturningModalError(
        tooLongPassword,
        tooLongPassword
      )
    ).toContain('A maximum of 256 characters is allowed here.')
  })

  test('users password can be changed to 256 characters', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const longestValidPassword = '1'.repeat(256)
    mockPremiumServer.expectUserUpdated(user, {
      password: longestValidPassword,
    })

    await ui.changePassword(longestValidPassword, longestValidPassword)

    await flushPromises()
  })

  test('changing a users password displays an error if the server responds with one', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const validPassword = '1'.repeat(8)

    testApp.dontFailOnErrorResponses()

    mockPremiumServer.expectUserUpdatedRespondsWithError(user, {
      error: 'ERROR_ADMIN_ONLY_OPERATION',
      detail: 'You do not have permission to perform this operation.',
    })

    const modal = await ui.changePassword(validPassword, validPassword)

    await flushPromises()

    expect(ui.getErrorText(modal)).toBe(
      "The action couldn't be completed because you don't have the right permissions."
    )
  })

  test('a users full name can be changed', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      fullName: 'Old Full Name',
    })

    const newFullName = 'New Full Name'
    mockPremiumServer.expectUserUpdated(user, {
      full_name: newFullName,
      // Expect the other edit modal fields will be sent, just with no changes.
      is_staff: user.is_staff,
      is_active: user.is_active,
      username: user.username,
    })

    await ui.changeFullName(newFullName)

    await flushPromises()

    const cells = ui.findCells()
    const { fullNameCell } = ui.getRow(cells, 0)
    expect(fullNameCell.text()).toContain(newFullName)
  })

  test('when an server error is returned when editing a user it is shown', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({})

    testApp.dontFailOnErrorResponses()

    mockPremiumServer.expectUserUpdatedRespondsWithError(user, {
      error: 'ERROR_ADMIN_ONLY_OPERATION',
      detail: 'You do not have permission to perform this operation.',
    })

    const modal = await ui.changeFullName('some terrible value')

    await flushPromises()

    expect(ui.getErrorText(modal)).toBe(
      "The action couldn't be completed because you don't have the right permissions."
    )
  })

  test('a users full name cant be changed to less than 2 characters', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const tooShortFullName = '1'

    const modal = await ui.changeFullName(tooShortFullName)
    const error = ui.getModalFieldErrorText(modal)

    expect(error).toContain(
      'Please enter a valid full name, it must be longer than 2 letters and less than 30.'
    )
  })

  test('a users full name cant be changed to more than 30 characters', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const tooLongFullName = '1'.repeat(31)

    const modal = await ui.changeFullName(tooLongFullName)
    const error = ui.getModalFieldErrorText(modal)

    expect(error).toContain(
      'Please enter a valid full name, it must be longer than 2 letters and less than 30.'
    )
  })

  test('a users username be changed', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      username: 'oldusername@example.com',
    })

    const newUserName = 'new_email@example.com'
    mockPremiumServer.expectUserUpdated(user, {
      username: newUserName,
      // Expect the other edit modal fields will be sent, just with no changes.
      full_name: user.full_name,
      is_staff: user.is_staff,
      is_active: user.is_active,
    })

    await ui.changeEmail(newUserName)

    await flushPromises()

    const cells = ui.findCells()
    const { usernameCell } = ui.getRow(cells, 0)
    expect(usernameCell.text()).toContain(newUserName)
  })

  test('a users username cannot be changed to a invalid email address', async () => {
    const { ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    const invalidEmail = '1'

    const modal = await ui.changeEmail(invalidEmail)
    const error = ui.getModalFieldErrorText(modal)

    expect(error).toContain('Please enter a valid e-mail address.')
  })
  test('a user can be set as staff ', async () => {
    await testToggleStaff(false)
  })

  test('a user can be unset as staff ', async () => {
    await testToggleStaff(true)
  })

  test('a user can be set as active ', async () => {
    await testToggleActive(false)
  })

  test('a user can be unset as active', async () => {
    await testToggleActive(true)
  })

  test('when there are fewer than 100 users the page buttons do nothing', async () => {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin()

    await ui.clickNextPage()
    await ui.clickNextPage()
    await ui.clickPrevPage()

    await flushPromises()

    expect(ui.getSingleRowUsernameText()).toContain(user.username)
  })

  test('when there are 2 pages of users the next and back buttons switch between them', async () => {
    const firstPageUser = mockPremiumServer.aUser({
      username: 'firstPageUser@example.com',
    })
    const secondPageUser = mockPremiumServer.aUser({
      username: 'secondPageUser@example.com',
    })
    mockPremiumServer.createUsers([firstPageUser], 1, { count: 150 })
    mockPremiumServer.createUsers([secondPageUser], 2, { count: 150 })

    const userAdmin = await testApp.mount(UsersAdminContent, {})
    const ui = new UserAdminUserHelpers(userAdmin)

    expect(ui.getSingleRowUsernameText()).toContain(firstPageUser.username)

    await ui.clickNextPage()
    await flushPromises()

    expect(ui.getSingleRowUsernameText()).toContain(secondPageUser.username)

    await ui.clickPrevPage()
    await flushPromises()

    expect(ui.getSingleRowUsernameText()).toContain(firstPageUser.username)
  })

  test('you can search by username which will pass the search text to the server', async () => {
    const firstUser = mockPremiumServer.aUser({
      id: 1,
      username: 'firstUser@example.com',
    })
    const secondUser = mockPremiumServer.aUser({
      id: 2,
      username: 'secondUser@example.com',
    })
    mockPremiumServer.createUsers([firstUser, secondUser], 1)
    mockPremiumServer.createUsers([firstUser], 1, { search: 'firstUser' })

    const userAdmin = await testApp.mount(UsersAdminContent, {})
    const ui = new UserAdminUserHelpers(userAdmin)

    const cells = ui.findCells(14)
    const { usernameCell: firstUsernameCell } = ui.getRow(cells, 0)
    expect(firstUsernameCell.text()).toContain('firstUser@example.com')
    const { usernameCell: secondUsernameCell } = ui.getRow(cells, 1)
    expect(secondUsernameCell.text()).toContain('secondUser@example.com')

    await ui.typeIntoSearchBox('firstUser')
    await flushPromises()

    expect(ui.getSingleRowUsernameText()).toContain(firstUser.username)
  })

  async function testToggleStaff(startingIsStaff) {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      isStaff: startingIsStaff,
    })

    let cells = ui.findCells()
    const { usernameCell } = ui.getRow(cells, 0)
    expect(ui.usernameCellIsForStaffMember(usernameCell)).toBe(startingIsStaff)

    mockPremiumServer.expectUserUpdated(user, {
      is_staff: !startingIsStaff,
      // Expect the other edit modal fields will be sent, just with no changes.
      username: user.username,
      full_name: user.full_name,
      is_active: user.is_active,
    })

    await ui.toggleIsStaff()

    await flushPromises()

    cells = ui.findCells()
    const { usernameCell: updatedUsernameCell } = ui.getRow(cells, 0)
    expect(ui.usernameCellIsForStaffMember(updatedUsernameCell)).toBe(
      !startingIsStaff
    )
  }

  async function testToggleActive(startingIsActive) {
    const { user, ui } = await whenThereIsAUserAndYouOpenUserAdmin({
      isActive: startingIsActive,
    })

    let cells = ui.findCells()
    const { isActiveCell } = ui.getRow(cells, 0)
    expect(isActiveCell.text()).toBe(
      startingIsActive ? 'Active' : 'Deactivated'
    )

    mockPremiumServer.expectUserUpdated(user, {
      is_active: !startingIsActive,
      // Expect the other edit modal fields will be sent, just with no changes.
      username: user.username,
      full_name: user.full_name,
      is_staff: user.is_staff,
    })

    await ui.toggleIsActive()

    await flushPromises()

    cells = ui.findCells()
    const { isActiveCell: updatedIsActiveCell } = ui.getRow(cells, 0)
    expect(updatedIsActiveCell.text()).toBe(
      startingIsActive ? 'Deactivated' : 'Active'
    )
  }

  async function whenThereIsAUserAndYouOpenUserAdmin(userSetup = {}) {
    const user = mockPremiumServer.aUser(userSetup)
    mockPremiumServer.createUsers([user], 1)

    const userAdmin = await testApp.mount(UsersAdminContent, {})
    const ui = new UserAdminUserHelpers(userAdmin)
    return { user, userAdmin, ui }
  }
})
