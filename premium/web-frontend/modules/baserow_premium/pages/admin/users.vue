<template>
  <UsersAdminContent></UsersAdminContent>
</template>

<script>
import { mapGetters } from 'vuex'

import { notifyIf } from '@baserow/modules/core/utils/error'
import UsersAdminContent from '@baserow_premium/components/UsersAdminContent'

export default {
  components: { UsersAdminContent },
  layout: 'app',
  middleware: 'staff',
  computed: {
    ...mapGetters({
      settings: 'settings/get',
    }),
  },
  methods: {
    async updateSettings(values) {
      try {
        await this.$store.dispatch('settings/update', values)
      } catch (error) {
        notifyIf(error, 'settings')
      }
    },
  },
}
</script>
