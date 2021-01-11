export class RealTimeHandler {
  constructor(context) {
    this.context = context
    this.socket = null
    this.connected = false
    this.reconnect = false
    this.reconnectTimeout = null
    this.events = {}
    this.attempts = 0
    this.registerCoreEvents()
  }

  /**
   * Creates a new connection with the web socket so that real time updates can be
   * received.
   */
  connect(reconnect = true) {
    this.reconnect = reconnect

    const token = this.context.store.getters['auth/token']

    // Because the web socket url is the same as the PUBLIC_BACKEND_URL apart from
    // the protocol.
    const url = new URL(this.context.app.$env.PUBLIC_BACKEND_URL)
    url.protocol = 'ws'
    url.pathname = '/ws/core/'

    this.socket = new WebSocket(`${url}?jwt_token=${token}`)
    this.socket.onopen = () => {
      this.context.store.dispatch('notification/setConnecting', false)
      this.connected = true
      this.attempts = 0
    }

    /**
     * The received messages are always JSON so we need to the parse it, extract the
     * type and call the correct event.
     */
    this.socket.onmessage = (message) => {
      let data = {}

      try {
        data = JSON.parse(message.data)
      } catch {
        console.log('Malformed message', message.data)
        return
      }

      if (
        Object.prototype.hasOwnProperty.call(data, 'type') &&
        Object.prototype.hasOwnProperty.call(this.events, data.type)
      ) {
        this.events[data.type](data, this.context)
      } else {
        console.log('Invalid message', message.data)
      }
    }

    /**
     * When the connection closes we want to reconnect immediately because we don't
     * want to miss any important real time updates. After the first attempt we want to
     * delay retry every 5 seconds.
     */
    this.socket.onclose = () => {
      this.connected = false

      // Automatically reconnect if the socket closes.
      if (this.reconnect) {
        this.attempts++
        this.context.store.dispatch('notification/setConnecting', true)

        setTimeout(
          () => {
            this.connect(true)
          },
          // After the first try, we want to try again every 5 seconds.
          this.attempts > 0 ? 5000 : 0
        )
      }
    }
  }

  /**
   * Disconnects the socket and resets all the variables. The can be used when
   * navigating to another page that doesn't require updates.
   */
  disconnect() {
    if (!this.connected) {
      return
    }

    this.context.store.dispatch('notification/setConnecting', false)
    clearTimeout(this.reconnectTimeout)
    this.reconnect = false
    this.attempts = 0
    this.connected = false
    this.socket.close()
  }

  /**
   * Registers a new event with the event registry.
   */
  registerEvent(type, callback) {
    this.events[type] = callback
  }

  /**
   * Registers all the core event handlers, which is for the groups and applications.
   */
  registerCoreEvents() {
    // When the authentication is succesful we want to store the web socket id in
    // auth store. Every AJAX request will include the web socket id as header, this
    // way the backend knows that this client does not has to receive the event
    // because we already know about the change.
    this.registerEvent('authentication', (data, { store }) => {
      store.dispatch('auth/setWebSocketId', data.web_socket_id)
    })

    this.registerEvent('group_created', (data, { store }) => {
      store.dispatch('group/forceCreate', data.group)
    })

    this.registerEvent('group_updated', (data, { store }) => {
      const group = store.getters['group/get'](data.group_id)
      if (group !== undefined) {
        store.dispatch('group/forceUpdate', { group, values: data.group })
      }
    })

    this.registerEvent('group_deleted', (data, { store }) => {
      const group = store.getters['group/get'](data.group_id)
      if (group !== undefined) {
        store.dispatch('group/forceDelete', group)
      }
    })

    this.registerEvent('application_created', (data, { store }) => {
      store.dispatch('application/forceCreate', { data: data.application })
    })

    this.registerEvent('application_updated', (data, { store }) => {
      const application = store.getters['application/get'](data.application_id)
      if (application !== undefined) {
        store.dispatch('application/forceUpdate', {
          application,
          data: data.application,
        })
      }
    })

    this.registerEvent('application_deleted', (data, { store }) => {
      const application = store.getters['application/get'](data.application_id)
      if (application !== undefined) {
        store.dispatch('application/forceDelete', application)
      }
    })
  }
}

export default function (context, inject) {
  inject('realtime', new RealTimeHandler(context))
}
