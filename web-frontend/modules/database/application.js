import { Application } from '@/core/applications'

export class DatabaseApplication extends Application {
  getType() {
    return 'database'
  }

  getIconClass() {
    return 'database'
  }

  getName() {
    return 'Database'
  }
}
