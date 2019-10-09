import ApplicationForm from '@/components/sidebar/ApplicationForm'

/**
 * The application base class that can be extended when creating a plugin for
 * the frontend.
 */
export class Application {
  /**
   * Must return a string with the unique name, this must be the same as the
   * type used in the backend.
   */
  getType() {
    return null
  }

  /**
   * The font awesome 5 icon name that is used as convenience for the user to
   * recognize certain application types. If you for example want the database
   * icon, you must return 'database' here. This will result in the classname
   * 'fas fa-database'.
   */
  getIconClass() {
    return null
  }

  /**
   * A human readable name of the application.
   */
  getName() {
    return null
  }

  /**
   * The form component that will be rendered when creating a new instance of
   * this application. By default the ApplicationForm component is returned, but
   * this only contains a name field. If custom fields are required upon
   * creating they can be added with this component.
   */
  getApplicationFormComponent() {
    return ApplicationForm
  }

  constructor() {
    this.type = this.getType()
    this.iconClass = this.getIconClass()
    this.name = this.getName()

    if (this.type === null) {
      throw Error('The type name of an application must be set.')
    }
    if (this.iconClass === null) {
      throw Error('The icon class of an application must be set.')
    }
    if (this.name === null) {
      throw Error('The name of an application must be set.')
    }
  }

  /**
   * @return object
   */
  serialize() {
    return {
      type: this.type,
      iconClass: this.iconClass,
      name: this.name
    }
  }
}
