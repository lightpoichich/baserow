import EditUserContext from '@baserow_premium/components/admin/user/EditUserContext'
import Error from '@baserow/modules/core/components/Error'
import ChangeUserPasswordModal from '@baserow_premium/components/admin/user/ChangeUserPasswordModal'
import EditUserModal from '@baserow_premium/components/admin/user/EditUserModal'
import CrudTableSearchContext from '@baserow_premium/components/crud_table/CrudTableSearchContext'
import CrudTableSearch from '@baserow_premium/components/crud_table/CrudTableSearch'

export default class UserAdminUserHelpers {
  constructor(userAdminComponent) {
    this.c = userAdminComponent
  }

  findCells(numCellsExpected = 7) {
    const cells = this.c.findAll('.crud-table-rows__cell')
    expect(cells.length).toBe(numCellsExpected)
    return cells
  }

  getRow(cells, rowNumber) {
    const offset = rowNumber * 7
    return {
      userIdCell: cells.at(offset),
      usernameCell: cells.at(offset + 1),
      fullNameCell: cells.at(offset + 2),
      groupsCell: cells.at(offset + 3),
      lastLoginCell: cells.at(offset + 4),
      signedUpCell: cells.at(offset + 5),
      isActiveCell: cells.at(offset + 6),
    }
  }

  getSingleRowUsernameText() {
    const cells = this.findCells()
    const { usernameCell } = this.getRow(cells, 0)
    return usernameCell.text()
  }

  getUsernameInitials(usernameCell) {
    const initials = usernameCell.get('.user-admin-rows__username--initials')
    return initials.text()
  }

  usernameCellIsForStaffMember(usernameCell) {
    return usernameCell.find('.user-admin-rows__username--icon').exists()
  }

  getGroups(groupsCell) {
    return groupsCell.findAll('.user-admin-rows__cell-group-item')
  }

  groupCellShowsThisUserIsGroupAdmin(groupCell) {
    return groupCell.find('.user-admin-rows__cell-group-icon').exists()
  }

  async openFirstUserActionsMenu() {
    await this.c.get('.user-admin-rows__username--menu').trigger('click')
    return this.c.findComponent(EditUserContext)
  }

  clickDeleteUser(editUserContext) {
    return editUserContext.find('.fa-trash-alt').trigger('click')
  }

  clickDeactivateUser(editUserContext) {
    return editUserContext.find('.fa-times').trigger('click')
  }

  clickActivateUser(editUserContext) {
    return editUserContext.find('.fa-check').trigger('click')
  }

  clickEditUser(editUserContext) {
    return editUserContext.find('.fa-pen').trigger('click')
  }

  clickChangeUserPassword(editUserContext) {
    return editUserContext.find('.fa-key').trigger('click')
  }

  async attemptToChangePasswordReturningModalError(password, repeatPassword) {
    const changePasswordModal = await this.changePassword(
      password,
      repeatPassword
    )

    return this.getModalFieldErrorText(changePasswordModal)
  }

  getModalFieldErrorText(modal) {
    return modal
      .find('.error')
      .text()
      .replace(/\n/gm, '')
      .replace(/\s\s+/g, ' ')
  }

  async changePassword(password, repeatPassword) {
    const editUserContext = await this.openFirstUserActionsMenu()

    await this.clickChangeUserPassword(editUserContext)

    const changePasswordModal = this.c.findComponent(ChangeUserPasswordModal)
    const passwordInputs = changePasswordModal.findAll('input')

    passwordInputs.at(0).element.value = password
    passwordInputs.at(0).trigger('input')
    passwordInputs.at(1).element.value = repeatPassword
    passwordInputs.at(1).trigger('input')

    await changePasswordModal.find('button').trigger('click')

    return changePasswordModal
  }

  getErrorText(component) {
    return component.findComponent(Error).find('.alert__content').text()
  }

  changeFullName(newFullName) {
    return this.changeUserEditField(newFullName, 0)
  }

  async changeUserEditField(newValue, inputIndex) {
    const editUserContext = await this.openFirstUserActionsMenu()

    await this.clickEditUser(editUserContext)

    const editUserModal = this.c.findComponent(EditUserModal)
    const userEditInputs = editUserModal.findAll('input')

    userEditInputs.at(inputIndex).element.value = newValue
    userEditInputs.at(inputIndex).trigger('input')

    await editUserModal.find('.button--primary').trigger('click')

    return editUserModal
  }

  async changeUserCheckbox(checkboxIndex) {
    const editUserContext = await this.openFirstUserActionsMenu()

    await this.clickEditUser(editUserContext)

    const editUserModal = this.c.findComponent(EditUserModal)
    const checkboxes = editUserModal.findAll('.checkbox')

    checkboxes.at(checkboxIndex).trigger('click')

    await editUserModal.find('button').trigger('click')

    return editUserModal
  }

  changeEmail(newEmail) {
    return this.changeUserEditField(newEmail, 1)
  }

  toggleIsStaff() {
    return this.changeUserCheckbox(1)
  }

  toggleIsActive() {
    return this.changeUserCheckbox(0)
  }

  clickNextPage() {
    return this.c.find('.fa-caret-right').trigger('click')
  }

  clickPrevPage() {
    return this.c.find('.fa-caret-left').trigger('click')
  }

  async typeIntoSearchBox(searchText) {
    const searchBox = this.c.findComponent(CrudTableSearch)
    await searchBox.find('a').trigger('click')
    const searchBoxContext = searchBox.findComponent(CrudTableSearchContext)
    const searchInput = searchBoxContext.find('input')
    searchInput.element.value = searchText
    await searchInput.trigger('input')
    await searchInput.trigger('keyup')
  }
}
