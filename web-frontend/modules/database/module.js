import path from 'path'

export default function DatabaseModule(options) {
  // Add the plugin to register the database application.
  this.addPlugin({
    src: path.resolve(__dirname, 'plugin.js'),
    filename: 'plugin.js'
  })
}
