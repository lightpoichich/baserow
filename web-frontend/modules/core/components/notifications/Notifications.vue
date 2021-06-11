<template>
  <div class="notifications">
    <div class="top-right-notifications">
      <ConnectingNotification v-if="connecting"></ConnectingNotification>
      <FailedConnectingNotification
        v-if="failedConnecting"
      ></FailedConnectingNotification>
      <Notification
        v-for="notification in normalNotifications"
        :key="notification.id"
        :notification="notification"
      ></Notification>
    </div>
    <div class="bottom-right-notifications">
      <UndoDeleteNotification
        v-for="notification in undoDeleteNotifications"
        :key="notification.id"
        :notification="notification"
      ></UndoDeleteNotification>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

import Notification from '@baserow/modules/core/components/notifications/Notification'
import ConnectingNotification from '@baserow/modules/core/components/notifications/ConnectingNotification'
import FailedConnectingNotification from '@baserow/modules/core/components/notifications/FailedConnectingNotification'
import UndoDeleteNotification from '@baserow/modules/core/components/notifications/UndoDeleteNotification'

export default {
  name: 'Notifications',
  components: {
    UndoDeleteNotification,
    Notification,
    ConnectingNotification,
    FailedConnectingNotification,
  },
  computed: {
    undoDeleteNotifications() {
      return this.notifications.filter((n) => n.type === 'undoDelete')
    },
    normalNotifications() {
      return this.notifications.filter((n) => n.type !== 'undoDelete')
    },
    ...mapState({
      connecting: (state) => state.notification.connecting,
      failedConnecting: (state) => state.notification.failedConnecting,
      notifications: (state) => state.notification.items,
    }),
  },
}
</script>
