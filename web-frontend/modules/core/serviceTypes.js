import { Registerable } from '@baserow/modules/core/registry'

export class ServiceType extends Registerable {
  get name() {
    throw new Error('Must be set on the type.')
  }

  /**
   * The integration type necessary to access this service.
   */
  get integrationType() {
    throw new Error('Must be set on the type.')
  }

  /**
   * The form component to edit this service.
   */
  get formComponent() {
    return null
  }

  /**
   * The collection element menu component.
   */
  get collectionElementMenuComponent() {
    return null
  }

  /**
   * A post-processor function for the collection element menu. The component
   * returned by `collectionElementMenuComponent` will return the raw filter,
   * sort and/or search value, and this function is responsible for processing
   * the value and turning it into a value we can add to our dispatch query.
   */
  collectionElementMenuPostProcessor(preProcessedValue) {
    return preProcessedValue
  }

  isValid(service) {
    return true
  }

  /**
   * Whether the service returns a collection of records.
   */
  get returnsList() {
    return false
  }

  /**
   * The maximum number of records that can be returned by this service
   */
  get maxResultLimit() {
    return 1
  }

  /**
   * Should return a JSON schema of the data returned by this service.
   */
  getDataSchema(applicationContext, service) {
    throw new Error('Must be set on the type.')
  }

  /**
   * A hook called prior to an update to modify the new values
   * before they get persisted in the API.
   */
  beforeUpdate(newValues, oldValues) {
    return newValues
  }

  /**
   * Returns a description of the given service
   */
  getDescription(service, application) {
    return this.name
  }

  getOrder() {
    return 0
  }
}
